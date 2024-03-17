# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass, field
from typing import final
import random

from .abstract_rps_player import AbstractRPSPlayer
from rps import rps_beat, RPS

__all__ = ['DoubleMarkovChainPlayer']


@final
@dataclass
class DoubleMarkovChainPlayer(AbstractRPSPlayer):
    """
    Memorize both the other player's moves and own player's moves to see how this compares
    to just memorizing the other player's moves.
    """
    chain_length: int = 1

    # Protected members to represent the transition matrix, i.e. given the player's last chain_length moves,
    # the counts of what they have played next.
    _transition_matrix: dict[tuple[tuple[RPS, ...], tuple[RPS, ...]], Counter[RPS]] = \
        field(init=False, default_factory=dict)

    # The last chain_length plays by the other player.
    _my_tuple: tuple[RPS, ...] = field(init=False, default_factory=tuple)
    _other_tuple: tuple[RPS, ...] = field(init=False, default_factory=tuple)

    def reset(self) -> None:
        self._transition_matrix.clear()
        self._other_tuple = ()
        self._my_tuple = ()

    def next_move(self) -> RPS:
        # If the tuple is too short, guess randomly.
        if len(self._other_tuple) < self.chain_length:
            return random.choice(list(RPS))

        # If the tuple has not yet been seen, guess randomly.
        values = self._transition_matrix.get((self._my_tuple, self._other_tuple))
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
        if len(self._my_tuple) != len(self._other_tuple):
            raise RuntimeError(f'{self.name} has gotten into an irregular state with uneven keys: '
                               f'{self._my_tuple}, {self._other_tuple}')

        # Record the new entry if we have a key of chain_length entries for the other player.
        if len(self._other_tuple) == self.chain_length:
            ctr = self._transition_matrix.setdefault((self._my_tuple, self._other_tuple), Counter())
            ctr[other] += 1

            # Update the tuples.
            self._my_tuple = self._my_tuple[1:] + (player,)
            self._other_tuple = self._other_tuple[1:] + (other,)
        else:
            self._my_tuple += (player,)
            self._other_tuple += (other,)

        if len(self._other_tuple) > self.chain_length:
            raise RuntimeError(f'{self.name} has key of length {len(self._other_tuple)}, max is {self.chain_length}.')
