# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass, field
from typing import final, Sequence

from .abstract_rps_player import AbstractRPSPlayer
from rps.rps import RPS

__all__ = ['PatternPlayer']


@final
@dataclass
class PatternPlayer(AbstractRPSPlayer):
    pattern: Sequence[RPS]
    _idx: int = field(init=False, default=0)

    def next_move(self) -> RPS:
        choice = self.pattern[self._idx]
        self._idx = (self._idx + 1) % len(self.pattern)
        return choice
