from LLMRoomEscape.Game import GameState
from LLMRoomEscape.IAgent import IAgent
from LLMRoomEscape.ToolRegistry import ToolRegistry
from pprint import pformat
import json

class AgentScripted(IAgent):
    def __init__(self, scriptedActions = []) -> None:
        super().__init__()
        self.scriptedActions = scriptedActions
        self.actionIdx = 0

    def reset(self):
        self.actionIdx = 0

    def pickAction(self, gameState: GameState, toolRegistry: ToolRegistry):
        action, action_args = self.scriptedActions[self.actionIdx]
        
        self.actionIdx += 1
        self.actionIdx = self.actionIdx % len(self.scriptedActions)

        return action, action_args