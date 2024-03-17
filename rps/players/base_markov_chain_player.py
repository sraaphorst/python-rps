# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from abc import abstractmethod
from collections import Counter
from dataclasses import dataclass, field
import random

from .abstract_rps_player import AbstractRPSPlayer
from rps.rps import rps_beat, rps_random, RPS

__all__ = ['BaseMarkovChainPlayer']


@dataclass
class BaseMarkovChainPlayer(AbstractRPSPlayer):
    chain_length: int = 1

    # _count_matrix keeps track of the counts of what was played by the opponent to determine
    # the probability of what to play next, i.e. it is a surrogate for the transition matrix.
    _count_matrix: dict[tuple[RPS, ...], Counter[RPS]] = field(init=False, default_factory=dict)

    # The states played by the other player.
    _other_tuple: tuple[RPS, ...] = field(init=False, default_factory=tuple)

    @abstractmethod
    def _get_transition_key(self) -> tuple[RPS, ...]:
        """
        Abstract method to create the key representing the state.
        """
        pass

    def reset(self) -> None:
        self._count_matrix.clear()
        self._other_tuple = ()

    def next_move(self) -> RPS:
        if len(self._other_tuple) < self.chain_length:
            return rps_random()

        key = self._get_transition_key()
        counts = self._count_matrix.get(key)
        if counts is None:
            return rps_random()

        total_plays = sum(counts.values())
        n = random.randrange(total_plays)

        cumulative = 0
        for rps, count in counts.items():
            cumulative += count
            if n < cumulative:
                return rps_beat(rps)

        raise ValueError(f'Could not determine next move for player {self.name}.')
