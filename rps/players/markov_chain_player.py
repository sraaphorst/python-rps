# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from collections import Counter
from dataclasses import dataclass
from typing import final

from .base_markov_chain_player import BaseMarkovChainPlayer
from rps.rps import RPS

__all__ = ['MarkovChainPlayer']


@final
@dataclass
class MarkovChainPlayer(BaseMarkovChainPlayer):
    """
    Markov chain player using the specified chain length, where the opponent's last moves
    form the key.
    """
    def _get_transition_key(self) -> tuple[RPS, ...]:
        return self._other_tuple

    def record_round(self, round_ct: int, player: RPS, other: RPS) -> None:
        if len(self._other_tuple) == self.chain_length:
            ctr = self._count_matrix.setdefault(self._other_tuple, Counter())
            ctr[other] += 1
            self._other_tuple = self._other_tuple[1:] + (other,)
        else:
            self._other_tuple += (other,)
