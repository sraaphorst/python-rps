# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from math import ceil, log10

from rps.common import get_all_pairs
from rps.match import *
from rps.players import *
from rps.rps import *


def main() -> None:
    ensemble_player = EnsemblePlayer(
        name='EnsemblePlayer',
        strategies=[
            DoubleMarkovChainPlayer(name='E-DM-1', chain_length=1),
            DoubleMarkovChainPlayer(name='E-DM-2', chain_length=2),
            DoubleMarkovChainPlayer(name='E-DM-3', chain_length=3),
            DoubleMarkovChainPlayer(name='E-DM-4', chain_length=4),
            BeatPreviousMovePlayer(name='E-BPM'),
            BeatenByPreviousMovePlayer(name='E-BBPM')
        ],
        deterministic=True
    )
    players = [
        ensemble_player,
        RandomPlayer(name='Random'),
        ConstantPlayer(name='Rock', symbol=RPS.ROCK),
        ConstantPlayer(name='Paper', symbol=RPS.PAPER),
        ConstantPlayer(name='Scissor', symbol=RPS.SCISSORS),
        BeatPreviousMovePlayer(name='BeatPreviousMove'),
        BeatenByPreviousMovePlayer(name='BeatenByPreviousMove'),
        PatternPlayer(name='RP', pattern=[RPS.ROCK, RPS.PAPER]),
        PatternPlayer(name='RPS', pattern=[RPS.ROCK, RPS.PAPER, RPS.SCISSORS]),
        MarkovChainPlayer(name='1-MarkovChain', chain_length=1),
        MarkovChainPlayer(name='2-MarkovChain', chain_length=2),
        MarkovChainPlayer(name='3-MarkovChain', chain_length=3),
        DoubleMarkovChainPlayer(name='1-DoubleMarkovChain', chain_length=1),
        DoubleMarkovChainPlayer(name='2-DoubleMarkovChain', chain_length=2),
        DoubleMarkovChainPlayer(name='3-DoubleMarkovChain', chain_length=3),
    ]

    nsp = max(len(p.name) for p in players)
    for p1, p2 in get_all_pairs(players):
        m = Match(p1, p2, 20000)
        print(f'***** {p1.name} vs {p2.name} *****')
        sp = ceil(log10(m.rounds)) + 1
        scores = m.play()
        for player, score in scores.items():
            print(f'\t{player:{nsp}} '
                  f'Wins: {score[Outcome.WIN]:>{sp}} '
                  f'Losses: {score[Outcome.LOSE]:>{sp}} '
                  f'Ties: {score[Outcome.TIE]:>{sp}}')


if __name__ == '__main__':
    main()
