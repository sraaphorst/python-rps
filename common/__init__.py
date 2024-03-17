# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from itertools import combinations
from typing import Generator, Sequence, TypeVar

__all__ = ['get_all_pairs']

T = TypeVar('T')


def get_all_pairs(seq: Sequence[T]) -> Generator[tuple[T, T], None, None]:
    for pair in combinations(seq, 2):
        yield pair
