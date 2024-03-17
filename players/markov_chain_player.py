# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass, field
from typing import final
import random

from .abstract_rps_player import AbstractRPSPlayer
from rps import rps_beat, RPS

__all__ = ['MarkovChainPlayer']


@final
@dataclass
class MarkovChainPlayer(AbstractRPSPlayer):
    chain_length: int = 1

    # Protected members to represent the transition matrix, i.e. given the player's last chain_length moves,
    # the counts of what they have played next.
    _transition_matrix: dict[tuple[RPS, ...], Counter[RPS]] = field(init=False, default_factory=dict)

    # The last chain_length plays by the other player.
    _played_tuple: tuple[RPS, ...] = field(init=False, default_factory=tuple)

    def reset(self) -> None:
        self._transition_matrix.clear()
        self._played_tuple = ()

    def next_move(self) -> RPS:
        # If the tuple is too short, guess randomly.
        if len(self._played_tuple) < self.chain_length:
            return random.choice(list(RPS))

        # If the tuple has not yet been seen, guess randomly.
        values = self._transition_matrix.get(self._played_tuple)
        if values is None:
            return random.choice(list(RPS))

        # Calculate the probability something will be played.
        total_plays = sum(values.values())
        n = random.randrange(total_plays)

        # Determine the predicted entry, and return what will beat it.
        cumulative = 0
        for rps, count in values.items():
            cumulative += count
            if n < cumulative:
                return rps_beat(rps)

        # We should never get here.
        raise ValueError(f'Could not determine next move for player {self.name}.')

    def record_round(self, round_ct: int, player: RPS, other: RPS) -> None:
        # Record the new entry if we have a key of chain_length entries for the other player.
        if len(self._played_tuple) == self.chain_length:
            ctr = self._transition_matrix.setdefault(self._played_tuple, Counter())
            ctr[other] += 1
            self._played_tuple = self._played_tuple[1:] + (other,)
        else:
            self._played_tuple += (other,)

        if len(self._played_tuple) > self.chain_length:
            raise RuntimeError(f'{self.name} has key of length {len(self._played_tuple)}, max is {self.chain_length}.')
