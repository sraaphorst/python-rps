# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass, field
from typing import final

from .base_markov_chain_player import BaseMarkovChainPlayer
from rps.rps import RPS

__all__ = ['DoubleMarkovChainPlayer']


@final
@dataclass
class DoubleMarkovChainPlayer(BaseMarkovChainPlayer):
    _my_tuple: tuple[RPS, ...] = field(init=False, default_factory=tuple)

    def _get_transition_key(self) -> tuple[RPS, ...]:
        return self._my_tuple + self._other_tuple

    def reset(self) -> None:
        super().reset()
        self._my_tuple = ()

    def record_round(self, round_ct: int, player: RPS, other: RPS) -> None:
        if len(self._my_tuple) != len(self._other_tuple):
            raise RuntimeError(f'{self.name} has uneven keys: {self._my_tuple}, {self._other_tuple}')

        if len(self._other_tuple) == self.chain_length:
            key = self._get_transition_key()
            ctr = self._count_matrix.setdefault(key, Counter())
            ctr[other] += 1

            self._my_tuple = self._my_tuple[1:] + (player,)
            self._other_tuple = self._other_tuple[1:] + (other,)
        else:
            self._my_tuple += (player,)
            self._other_tuple += (other,)
