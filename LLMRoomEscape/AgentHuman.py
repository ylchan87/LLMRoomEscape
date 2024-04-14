from Game import GameState
from IAgent import IAgent
from LLMRoomEscape.ToolRegistry import ToolRegistry
from pprint import pformat
import json

class AgentHuman(IAgent):
    def pickAction(self, gameState: GameState, toolRegistry: ToolRegistry):
        locations = [f"- {l}" for l in gameState.locations]
        locations = "\n".join(locations)

        player_inventory = [f"- {i.name} : {i.description}" for i in gameState.player_inventory]
        player_inventory = "\n".join(player_inventory)
        if player_inventory == "": player_inventory = "Nothing"

        tool_descriptions = toolRegistry.get_tool_descriptions()
        tool_descriptions = pformat(tool_descriptions)

        player_history = [f"tried {action} with argument {args} and get result {result}" for action, args, result in gameState.player_history]
        player_history = "\n".join(player_history)
        if player_history == "": player_history = "Nothing"

        prompt = \
f"""
You are locked in a room, and you need to escape.

Around you, you see.
{locations}

In your inventory you have
{player_inventory}

Possible actions are:
{tool_descriptions}

The past actions you have are:
{player_history}
"""
        print(prompt)
        action = input("Enter your chosen action as str:")

        while True:
            try:
                action_args = input("Enter your action arguments as json dict as str:")
                action_args = json.loads(action_args)
                break
            except json.JSONDecodeError:
                print("Invalid json. Try again")
                continue

        return action, action_args