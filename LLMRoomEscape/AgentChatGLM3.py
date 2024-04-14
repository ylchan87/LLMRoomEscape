from Game import GameState
from IAgent import IAgent
from LLMRoomEscape.ToolRegistry import ToolRegistry
from pprint import pformat, pprint
import json
import os
from transformers import AutoTokenizer, AutoModel

MODEL_PATH = os.environ.get('MODEL_PATH', 'THUDM/chatglm3-6b')
TOKENIZER_PATH = os.environ.get("TOKENIZER_PATH", MODEL_PATH)

tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_PATH, trust_remote_code=True)
model = AutoModel.from_pretrained(MODEL_PATH, trust_remote_code=True, device_map="auto").eval()

class AgentChatGLM3(IAgent):
    def __init__(self, debug=False) -> None:
        super().__init__()
        self.debug = debug

    def pickAction(self, gameState: GameState, toolRegistry: ToolRegistry):
        locations = [f"- {l}" for l in gameState.locations]
        locations = "\n".join(locations)

        player_inventory = [f"- {i.name} : {i.description}" for i in gameState.player_inventory]
        player_inventory = "\n".join(player_inventory)
        if player_inventory == "": player_inventory = "Nothing"

        tool_descriptions = toolRegistry.get_tool_descriptions()

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

The past actions you have are:
{player_history}

You have access to the following tools:
"""

        llm_history = [
            {
                "role": "system",
                "content": prompt,
                "tools": tool_descriptions
            },
        ]
        
        while True:
            try:
                pprint(llm_history)

                query = 'what is the your action? You must use one of the tools'
                response, history = model.chat(tokenizer, query, history=llm_history, role="user")

                print(response)
                if self.debug:
                    human_response = input("Enter to accept LLM's response / Type to override:")
                    if human_response != "": response = human_response

                if type(response) != dict:
                    response = json.loads(response)

                action      = response["name"]
                action_args = response["parameters"]
                break
            except json.JSONDecodeError:
                print("Invalid json. Try again")
                continue

        return action, action_args