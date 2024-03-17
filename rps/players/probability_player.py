# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass, field
from math import fabs
from typing import final, ClassVar

from .abstract_player import AbstractPlayer
from rps.common import probability_selector
from rps.rps import rps_random, RPS

__all__ = [
    'ProbabilityPlayer',
    'RandomPlayer',
    'ConstantPlayer',
]


@dataclass
class ProbabilityPlayer(AbstractPlayer):
    probability_map: dict[RPS, float]

    # Threshold for probability to vary from 1.
    _threshold: ClassVar[float] = field(init=False, default=1e-6)

    def __post_init__(self):
        if fabs(sum(self.probability_map.values()) - 1) > self._threshold:
            raise ValueError(f'Probability map does not sum to 1: {self.probability_map}')

    def next_move(self, round_number: int) -> RPS:
        move = probability_selector(self.probability_map)
        return move if move is not None else rps_random()


@final
class RandomPlayer(ProbabilityPlayer):
    def __init__(self, name: str):
        super().__init__(name=name, probability_map={RPS.ROCK: 1.0 / 3.0,
                                                     RPS.PAPER: 1.0 / 3.0,
                                                     RPS.SCISSORS: 1.0 / 3.0})


@final
class ConstantPlayer(ProbabilityPlayer):
    def __init__(self, name: str, symbol: RPS):
        super().__init__(name=name, probability_map={symbol: 1.0})
