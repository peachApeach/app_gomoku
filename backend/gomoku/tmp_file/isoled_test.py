import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
from little_gomoku_utils import convert_to_little_gomoku

gomoku = Gomoku()

littleGomoku = convert_to_little_gomoku(gomoku)
littleGomoku.place_stone(4, 9)
littleGomoku.switch_player_turn()
littleGomoku.place_stone(5, 9)

print(littleGomoku.get_actions())
littleGomoku.paint_actions(littleGomoku.get_actions())
print(littleGomoku)

