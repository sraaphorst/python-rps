# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass
from typing import final, Callable, Optional

from .abstract_player import AbstractPlayer
from rps.rps import rps_beater, rps_beating, rps_random, RPS

__all__ = [
    'PreviousSymbolFunctionPlayer',
    'BeatPreviousMovePlayer',
    'BeatenByPreviousMovePlayer',
]


@dataclass
class PreviousSymbolFunctionPlayer(AbstractPlayer):
    """
    A player that invokes a function based on the last symbol played by the opponent to determine
    the next symbol to play.
    """
    function: Callable[[RPS], RPS]
    _previous_move: Optional[RPS] = None

    def next_move(self, round_number: int) -> RPS:
        if self._previous_move is None:
            return rps_random()
        return self.function(self._previous_move)

    def record_round(self, round_number: int, player_symbol: RPS, opponent_symbol: RPS) -> None:
        self._previous_move = opponent_symbol


@final
@dataclass
class BeatPreviousMovePlayer(PreviousSymbolFunctionPlayer):
    def __init__(self, name: str):
        super().__init__(name=name, function=rps_beater)


@final
@dataclass
class BeatenByPreviousMovePlayer(PreviousSymbolFunctionPlayer):
    def __init__(self, name: str):
        super().__init__(name=name, function=rps_beating)
