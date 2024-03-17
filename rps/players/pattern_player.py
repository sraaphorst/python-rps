# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from dataclasses import dataclass, field
from typing import final, Callable, Sequence

from .abstract_player import *

__all__ = [
    'FunctionPlayer',
    'PatternPlayer',
]


@dataclass
class FunctionPlayer(AbstractPlayer):
    """
    A flexible pattern player that takes a function that, given the round number, returns a symbol.
    This could represent anything including a random pattern, so it is too generic to learn.
    We create some implementations of it below to try out recognition strategies in specific instances.
    """
    symbol_producer: Callable[[int], RPS]

    def next_move(self, round_number: int) -> RPS:
        return self.symbol_producer(round_number)


@final
@dataclass
class PatternPlayer(FunctionPlayer):
    """
    An implementation of FunctionPlayer that allows for a pattern that:
    1. Has an initial pattern.
    2. Then has a pattern that cycles beyond what a fixed-length Markov chain could recognize.
    """
    def __init__(self, name: str, pattern: Sequence[RPS]):
        super().__init__(name, lambda x: pattern[x % len(pattern)])
