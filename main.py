# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from math import ceil, log10

from rps.common import get_all_pairs
from rps.match import *
from rps.players import *
from rps.rps import *


def main() -> None:
    players = [
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
        MarkovChainPlayer(name="3-MarkovChain", chain_length=3),
        DoubleMarkovChainPlayer(name="1-DoubleMarkovChain", chain_length=1),
        DoubleMarkovChainPlayer(name="2-DoubleMarkovChain", chain_length=2),
        DoubleMarkovChainPlayer(name="3-DoubleMarkovChain", chain_length=3),
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

# Others:
# Play with probabilities - generalization of random, which is just default values 1/3.
# Play last player's move.
# Play the move that is not the last player's move and would not beat the last player's move.