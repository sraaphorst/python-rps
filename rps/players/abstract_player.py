# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rps.rps import RPS


@dataclass
class AbstractPlayer(ABC):
    """
    Generic interface to be implemented by an RPS player.
    """
    name: str

    def reset(self) -> None:
        """
        Reset the player, clearing out any internal data.
        """
        pass

    @abstractmethod
    def next_move(self, round_number: int) -> RPS:
        """
        Prompt the player for a next move.
        """
        pass

    def record_round(self, round_number: int, player_symbol: RPS, opponent_symbol: RPS) -> None:
        """
        Record the details of a round.
        Provides the move made by this player and the other player.
        """
        pass
