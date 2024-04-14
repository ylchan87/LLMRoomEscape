import random
from typing import Annotated
from LLMRoomEscape.ToolRegistry import *
from Game import GameItem, GameState, GameLogic, game_loop

if __name__ == "__main__":
    gameState = GameState()
    gameLogic = GameLogic(gameState)

    # from AgentHuman import AgentHuman
    # player    = AgentHuman()

    from AgentChatGLM3 import AgentChatGLM3
    player    = AgentChatGLM3(debug=True)

    game_loop(player, gameLogic, gameState)
    
    print("You escaped the room!")