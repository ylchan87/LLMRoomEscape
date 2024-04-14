import random
from typing import Annotated
from LLMRoomEscape.ToolRegistry import *
from Game import GameItem, GameState, GameLogic, game_loop
from AgentHuman import AgentHuman

if __name__ == "__main__":
    gameState = GameState()
    gameLogic = GameLogic(gameState)
    player    = AgentHuman()
    game_loop(player, gameLogic, gameState)
    
    print("You escaped the room!")