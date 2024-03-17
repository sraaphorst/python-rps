# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass
from typing import final, Final

from rps.players import AbstractRPSPlayer
from rps.rps import rps_compare, Outcome

default_rounds: Final[int] = 1000


@final
@dataclass
class Match:
    player1: AbstractRPSPlayer
    player2: AbstractRPSPlayer
    rounds: int = default_rounds

    def __post_init__(self):
        if self.player1.name == self.player2.name:
            raise ValueError(f'Players have the same name: "{self.player1.name}"')

    def play(self) -> dict[str, Counter[Outcome]]:
        """
        Return the scores for each of the two players by their name.
        """
        # Reset the players.
        self.player1.reset()
        self.player2.reset()

        # Reset the Counter.
        p1_scores: Counter[Outcome] = Counter()
        p2_scores: Counter[Outcome] = Counter()

        for round_ct in range(self.rounds):
            move1 = self.player1.next_move()
            move2 = self.player2.next_move()
            self.player1.record_round(round_ct, move1, move2)
            self.player2.record_round(round_ct, move2, move1)

            p1_scores[rps_compare(move1, move2)] += 1
            p2_scores[rps_compare(move2, move1)] += 1

        return {self.player1.name: p1_scores, self.player2.name: p2_scores}
