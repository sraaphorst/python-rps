# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from itertools import combinations
from typing import Generator, Mapping, Optional, Sequence, TypeVar
import random

__all__ = [
    'get_all_pairs',
    'probability_selector',
]


T = TypeVar('T')


def get_all_pairs(seq: Sequence[T]) -> Generator[tuple[T, T], None, None]:
    for pair in combinations(seq, 2):
        yield pair


def probability_selector(probability_map: Mapping[T, float]) -> Optional[T]:
    prob = random.random()
    cumulative = 0
    for key, value in probability_map.items():
        cumulative += value
        if prob < cumulative:
            return key

    # If we reach here, we fell into a tiny epsilon at the end.
    return None
