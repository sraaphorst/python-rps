# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from typing import final
import random

from .abstract_rps_player import AbstractRPSPlayer
from rps import RPS

__all__ = ['RandomPlayer']


@final
class RandomPlayer(AbstractRPSPlayer):
    def next_move(self) -> RPS:
        return random.choice(list(RPS))
