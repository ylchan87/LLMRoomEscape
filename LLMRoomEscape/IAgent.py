from abc import ABC, abstractmethod
from LLMRoomEscape.ToolRegistry import ToolRegistry
from LLMRoomEscape.Game import GameState

class IAgent(ABC):
    @abstractmethod
    def pickAction(gameState:GameState, toolRegistry:ToolRegistry):
        pass
