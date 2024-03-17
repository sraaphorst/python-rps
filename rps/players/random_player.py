# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from typing import final

from .abstract_rps_player import AbstractRPSPlayer
from rps.rps import rps_random, RPS

__all__ = ['RandomPlayer']


@final
class RandomPlayer(AbstractRPSPlayer):
    def next_move(self) -> RPS:
        return rps_random()
