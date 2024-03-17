# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass, field, InitVar
from typing import final, Optional

from .abstract_player import AbstractPlayer
from rps.common import probability_selector
from rps.rps import rps_compare, Outcome, RPS

__all__ = ['EnsemblePlayer']


@final
@dataclass(frozen=True)
class StrategyConfidence:
    # P(A_i) as described below.
    str_prob: float

    # P(T|A_i) as described below.
    sym_cond_prob: dict[RPS, float]


@final
@dataclass
class EnsembleRecord:
    strategy: AbstractPlayer
    guesses: dict[Outcome, Counter[RPS]] = field(init=False, default_factory=dict)

    def reset(self):
        """
        Resets the entire EnsembleRecord, including the strategy, confidence_level, and next_guess.
        """
        self.strategy.reset()
        self.guesses = {outcome: Counter() for outcome in Outcome}

    def next_guess(self, round_num: int) -> RPS:
        return self.strategy.next_move(round_num)

    def record_round(self, round_number: int, player_symbol: RPS, opponent_symbol: RPS) -> None:
        """
        Records the impact of the current guess for this strategy and its impact on the
        confidence of the strategy.
        """
        self.strategy.record_round(round_number, player_symbol, opponent_symbol)

        outcome = rps_compare(player_symbol, opponent_symbol)
        self.guesses[outcome][player_symbol] += 1

    def determine_confidence(self) -> StrategyConfidence:
        """
        For this strategy A, determine P(A) and P(T|A) as above for T in RPS.
        """
        # Calculate the confidence level P(A) for this strategy.
        # If there have been no wins or losses, use a default of 0.5 to indicate no known information.
        wins = sum(self.guesses[Outcome.WIN].values())
        losses = sum(self.guesses[Outcome.LOSE].values())
        str_prob = 0.5 if wins + losses == 0 else wins / (wins + losses)

        # Calculate the probability for each symbol T given A, i.e. P(T|A).
        sym_cond_prob: dict[RPS, float] = {}
        for sym in RPS:
            correct_sym_guesses = self.guesses[Outcome.WIN][sym]
            total_sym_guesses = sum(self.guesses[outcome][sym] for outcome in Outcome)
            sym_cond_prob[sym] = correct_sym_guesses / total_sym_guesses if total_sym_guesses else 0.5

        return StrategyConfidence(str_prob=str_prob,
                                  sym_cond_prob=sym_cond_prob)


@final
@dataclass
class EnsemblePlayer(AbstractPlayer):
    """
    Uses an ensemble of strategies to predict the next winning move.
    Let A_0, ..., A_{n-1} be the strategies.

    We use a rough Bayesian formula to determine the guess for round n.
    For a strategy A_i, we calculate:
    P(A_i) = 0.5                  if n == 0 or wins + losses = 0 for A_i (no rounds or all rounds are ties)
           = wins / (wins + losses) otherwise

    For each symbol T in {R, P, S}:
    P(T|A_i) = # times T was guessed correctly by A_i / # times T was guessed by A_i

    Let G(A_i, n, T) = 1 if the winning move guessed by A_i is T
                       0 otherwise

    For the ensemble of strategies A_0, ... A_{n-1}, this gives a total of:
    P(T) = sum_i G(Ai, n, T) * P(T|A_i) * P(A_i)

    We then normalize to get a number in [0, 1].
    P'(T) = P(T) / (P(R) + P(P) + P(S).

    If we opt for a deterministic approach, we pick the T with the largest value of P'(T).
    Simple, makes decisions based on strongest evidence, but might become predictable over time.

    If we opt for a random selection, we use these as probabilities to determine our choice.
    Stochastic, and thwarts and adaptive opponent. May pick suboptimal choice.
    """
    strategies: InitVar[list[AbstractPlayer]]
    deterministic: bool = False
    _ensemble_records: list[EnsembleRecord] = field(init=False)
    _current_guesses: list[Optional[RPS]] = field(init=False)

    def __post_init__(self, strategies: list[AbstractPlayer]):
        self._ensemble_records = [EnsembleRecord(strategy) for strategy in strategies]
        self._current_guesses = [None] * len(self._ensemble_records)

    def reset(self) -> None:
        for ensemble_record in self._ensemble_records:
            ensemble_record.reset()

    def next_move(self, round_number: int) -> RPS:
        # Get the next guesses for each strategy.
        self._current_guesses = []

        # Combine the confidences for each strategy to come up with a probability for each move.
        sym_confidence = {sym: 0 for sym in RPS}
        for ensemble_record in self._ensemble_records:
            guess = ensemble_record.next_guess(round_number)
            self._current_guesses.append(guess)
            str_confidence = ensemble_record.determine_confidence()

            # Adjust the confidence for this strategy for the guess to give it a score.
            sym_confidence[guess] += str_confidence.str_prob * str_confidence.sym_cond_prob[guess]

        # Normalize the levels.
        sym_confidence_sum = sum(sym_confidence.values())
        sym_probability: dict[RPS, float] = {}
        for sym in RPS:
            sym_probability[sym] = sym_confidence[sym] / sym_confidence_sum if sym_confidence_sum else 0.5

        if self.deterministic:
            return max(sym_probability, key=sym_probability.get)
        else:
            return probability_selector(sym_probability)

    def record_round(self, round_number: int, player_symbol: RPS, opponent_symbol: RPS) -> None:
        """
        For each strategy, record the round and update the confidence in that strategy
        and the guess which it made.
        """
        for ensemble_record, guess in zip(self._ensemble_records, self._current_guesses):
            ensemble_record.record_round(round_number, guess, opponent_symbol)
