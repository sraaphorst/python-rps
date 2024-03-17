# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass
from typing import final

from .abstract_rps_player import AbstractRPSPlayer
from rps import RPS

__all__ = ["ConstantPlayer"]


@final
@dataclass
class ConstantPlayer(AbstractRPSPlayer):
    """
    A player that constantly plays only one move.
    """
    move: RPS

    def next_move(self) -> RPS:
        return self.move
