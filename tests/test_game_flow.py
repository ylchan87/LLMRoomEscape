import unittest

from LLMRoomEscape.Game import GameState, GameLogic, game_loop
from LLMRoomEscape.ToolRegistry import ToolRegistry
from LLMRoomEscape.AgentScripted import AgentScripted

class TestGameFlow(unittest.TestCase):
    def setUp(self):
        self.gameState = GameState()
        self.gameLogic = GameLogic(self.gameState)
        

    def test_box_needs_key(self):

        self.gameState.reset()
        
        player = AgentScripted([
            ("inspect"    , {'location': 'Bed'}),  # get box
            ("unlock_box" , {}),
        ])

        game_loop(player, self.gameLogic, self.gameState, maxIter=10)
        self.assertEqual("Paper" in self.gameState.player_inventory, False)


    def test_can_escape(self):

        self.gameState.reset()
        self.gameState.door_pw

        player = AgentScripted([
            ("inspect"    , {'location': 'Bed'}),
            ("inspect"    , {'location': 'Drawer'}),
            ("unlock_box" , {}),
            ("unlock_door", {'password': self.gameState.door_pw}),
        ])

        game_loop(player, self.gameLogic, self.gameState, maxIter=10)
        self.assertEqual(self.gameState.door_opened, True)

if __name__ == '__main__':
    unittest.main()
