# Copyright (c) 2024 Sebastian Raaphorst.
# For license information see LICENSE or https://opensource.org/licenses/BSD-3-Clause

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rps.rps import RPS


@dataclass
class AbstractRPSPlayer(ABC):
    name: str

    """
    Generic interface to be implemented by an RPS player.
    """
    @abstractmethod
    def next_move(self) -> RPS:
        """
        Prompt the player for a next move.
        """
        pass

    def reset(self) -> None:
        """
        Reset the player, clearing out any internal data.
        """
        pass

    def record_round(self, round_ct: int, player: RPS, other: RPS) -> None:
        """
        Record the details of a round.
        Provides the move made by this player and the other player.
        """
        pass
