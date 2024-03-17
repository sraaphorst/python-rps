# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass
from typing import final, Optional

from .abstract_rps_player import AbstractRPSPlayer
from rps.rps import rps_beat, rps_random, RPS

__all__ = ['BeatPreviousMovePlayer']


@final
@dataclass
class BeatPreviousMovePlayer(AbstractRPSPlayer):
    """
    A player that always plays a move that would have beaten the opponent's previous move.
    """
    _previous_move: Optional[RPS] = None

    def next_move(self) -> RPS:
        if self._previous_move is None:
            return rps_random()
        return rps_beat(self._previous_move)

    def record_round(self, round_ct: int, player: RPS, other: RPS) -> None:
        self._previous_move = other
