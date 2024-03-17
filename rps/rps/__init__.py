# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from enum import Enum, IntEnum
from typing import final
import random


__all__ = [
    'Outcome',
    'RPS',
    'rps_random',
    'rps_beat',
    'rps_compare',
]


@final
class Outcome(IntEnum):
    """
    Possible outcomes of matches, and their score.
    """
    LOSE = -1
    TIE = 0
    WIN = 1


@final
class RPS(Enum):
    """
    The choices of symbols to pick.
    """
    ROCK = 'R'
    PAPER = 'P'
    SCISSORS = 'S'


def rps_random() -> RPS:
    """
    Return a random symbol.
    """
    return random.choice(list(RPS))


def rps_beat(rps: RPS) -> RPS:
    """
    Given a symbol, determine what will beat it.
    """
    match rps:
        case RPS.ROCK: return RPS.PAPER
        case RPS.PAPER: return RPS.SCISSORS
        case RPS.SCISSORS: return RPS.ROCK


def rps_compare(a: RPS, b: RPS) -> Outcome:
    """
    Given a play of two symbols, return the outcome of the first when compared to the second.
    """
    match (a, b):
        case (RPS.ROCK, RPS.PAPER): return Outcome.LOSE
        case (RPS.ROCK, RPS.SCISSORS): return Outcome.WIN
        case (RPS.PAPER, RPS.ROCK): return Outcome.WIN
        case (RPS.PAPER, RPS.SCISSORS): return Outcome.LOSE
        case (RPS.SCISSORS, RPS.ROCK): return Outcome.LOSE
        case (RPS.SCISSORS, RPS.PAPER): return Outcome.WIN
        case _: return Outcome.TIE
