# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from math import ceil, log10

from common import get_all_pairs
from match import *
from players import *
from rps import *


def main() -> None:
    players = [
        RandomPlayer(name='RandomPlayer'),
        ConstantPlayer(name='RockPlayer', move=RPS.ROCK),
        ConstantPlayer(name='PaperPlayer', move=RPS.PAPER),
        ConstantPlayer(name='ScissorPlayer', move=RPS.SCISSORS),
        PatternPlayer(name='RPPlayer', pattern=[RPS.ROCK, RPS.PAPER]),
        PatternPlayer(name='RPSPlayer', pattern=[RPS.ROCK, RPS.PAPER, RPS.SCISSORS]),
        MarkovChainPlayer(name='1-MarkovChainPlayer', chain_length=1),
        MarkovChainPlayer(name='2-MarkovChainPlayer', chain_length=2),
        MarkovChainPlayer(name="3-MarkovChainPlayer", chain_length=3),
        DoubleMarkovChainPlayer(name="1-DoubleMarkovChainPlayer", chain_length=1),
        DoubleMarkovChainPlayer(name="2-DoubleMarkovChainPlayer", chain_length=2),
        DoubleMarkovChainPlayer(name="3-DoubleMarkovChainPlayer", chain_length=3),
    ]

    nsp = max(len(p.name) for p in players)
    for p1, p2 in get_all_pairs(players):
        m = Match(p1, p2)
        print(f'*** {p1.name} vs {p2.name} ***')
        sp = ceil(log10(m.rounds)) + 1
        scores = m.play()
        for player, score in scores.items():
            print(f'\t{player:{nsp}}: '
                  f'Wins: {score[Outcome.WIN]:>{sp}} '
                  f'Losses: {score[Outcome.LOSE]:>{sp}} '
                  f'Ties: {score[Outcome.TIE]:>{sp}}')


if __name__ == "__main__":
    main()
