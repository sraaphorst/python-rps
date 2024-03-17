# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass, field
from math import fabs
from typing import final, ClassVar
import random

from .abstract_rps_player import AbstractRPSPlayer
from rps.rps import rps_random, RPS

__all__ = [
    'ProbabilityPlayer',
    'RandomPlayer',
    'ConstantPlayer',
]


@dataclass
class ProbabilityPlayer(AbstractRPSPlayer):
    probability_map: dict[RPS, float]

    # Threshold for probability to vary from 1.
    _threshold: ClassVar[float] = field(init=False, default=1e-6)

    def __post_init__(self):
        if fabs(sum(self.probability_map.values()) - 1) > self._threshold:
            raise ValueError(f'Probability map does not sum to 1: {self.probability_map}')

    def next_move(self) -> RPS:
        prob = random.random()
        cumulative = 0
        for key, value in self.probability_map.items():
            cumulative += value
            if prob < cumulative:
                return key

        # If there is a slight deviation in probabilities, return a random value.
        return rps_random()


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
