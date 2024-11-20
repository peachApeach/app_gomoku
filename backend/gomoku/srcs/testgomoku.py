
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Gomoku import Gomoku
from algorithms.gomoku_algorithm import minimax
from utils.little_gomoku_utils import convert_to_little_gomoku
from utils.gomoku_utils import convert_xy_to_coordinate, convert_coordinate_to_xy
from LittleGomoku import LittleGomoku

gomoku = Gomoku()
gomoku.player_turn = "B"
gomoku.board = [
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," ","W"," ","W","W"," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," ","B"," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," ","W"," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," ","W"," ","W"," ","W"," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
		[" "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "," "],
	]

print(gomoku)


score, move = minimax(convert_to_little_gomoku(gomoku), MAX_DEPTH=2)

print(gomoku.player_turn)
print(gomoku.maximizing_player)
print(gomoku.minimizing_player)
print(score)
print(move)
print(convert_xy_to_coordinate(move[1], move[0]))


s1 = convert_to_little_gomoku(gomoku).simulate_action((convert_coordinate_to_xy("K8")[1], convert_coordinate_to_xy("K8")[0]))
print(s1)

score, move = minimax(s1, MAX_DEPTH=1)
print(score)
print(move)
print(convert_xy_to_coordinate(move[1], move[0]))


s2 = s1.simulate_action((convert_coordinate_to_xy("P9")[1], convert_coordinate_to_xy("P9")[0]))
print(s2)

print(s2.free_four_white)
# print(convert_xy_to_coordinate(convert_coordinate_to_xy("K8")[0], convert_coordinate_to_xy("K8")[1]))
# s1.paint_actions(s1.get_actions())
