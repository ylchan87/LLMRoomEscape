import random
from typing import Annotated, List, Tuple
from LLMRoomEscape.ToolRegistry import *

class GameItem:
    def __init__(self, name="sword", description="shiny sword", location=None) -> None:
        self.name        = name
        self.description = description
        self.location    = location

class GameState:
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        random_int = int(random.random()*9999)

        self.door_pw     = f"{random_int:0>4}"
        self.door_opened = False

        self.game_items = {
            "Key"   : GameItem("Key"  ,  "A fancy blue key",          "Drawer"),
            "Box"   : GameItem("Box"  ,  "A fancy blue treasure box", "Bed"),
            "Paper" : GameItem("Paper", f"A piece of paper with '{self.door_pw}' written on it", "Box"),
        }

        self.player_inventory : List[GameItem] = []
        self.player_history   : List[Tuple[str,str,str]] = []  # action, action_args, result

        self.locations = ["Bed", "Drawer"]

class GameLogic:
    def __init__(self, gameState: GameState) -> None:
        self.game_state = gameState
    
    def inspect(self, 
                location: Annotated[str, 'The location to inspect', True],
            ):
        """
        inspect a location
        """
        if location not in self.game_state.locations:
            return f"No {location} is around"
        
        result = ""
        for key,item in self.game_state.game_items.items():
            if item.location == location:
                result += f"You found a {item.name}\n"
                item.location = "Inventory"
                self.game_state.player_inventory.append(item)

        return result
    
    def unlock_door(self, 
                    password: Annotated[str, 'The password for the door', True],
                ):
        """
        try unlock the main door of the room
        """
        if password != self.game_state.door_pw:
            return "Password is wrong"
        else:
            self.game_state.door_opened = True
            return "Door is opened"
        
    
    def unlock_box(self):
        """
        try unlock the main door of the room
        """
        box   = self.game_state.game_items["Box"]
        key   = self.game_state.game_items["Key"]
        paper = self.game_state.game_items["Paper"]
        if box not in self.game_state.player_inventory:
            return "You don't have a box"
        elif key not in self.game_state.player_inventory:
            return "You don't have key for opening the box"
        else:
            self.game_state.player_inventory.append(paper)
            return f"You opened the box with your key and found a {paper.name}"

    def get_possible_actions(self):
        possible_actions = [
            self.inspect,
            self.unlock_door,
        ]

        box = self.game_state.game_items["Box"]
        if box in self.game_state.player_inventory:
            possible_actions.append(self.unlock_box)
            
        return possible_actions



def game_loop(player, gameLogic, gameState, maxIter = 9999):
    
    for i in range(maxIter):
        tr = ToolRegistry("PlayerActions") 
        for a in gameLogic.get_possible_actions():
            tr.register_tool(a)

        action, action_args = player.pickAction(gameState, tr)
        result = tr.dispatch_tool(action, action_args)

        gameState.player_history.append( (action, action_args, result))
