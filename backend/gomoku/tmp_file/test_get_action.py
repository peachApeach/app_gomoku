import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
from gomoku_algorithm import minimax
from little_gomoku_utils import convert_to_little_gomoku
from MeasureTime import MeasureTime

if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.read_a_game(9, -11, live_visualisation=False, live_speed=0.5)
	print(gomoku)
	littleGomoku = convert_to_little_gomoku(gomoku)
	mt = MeasureTime(start=True)
	score, move = minimax(gomoku=littleGomoku, MAX_DEPTH=2)
	mt.stop()
	# DEPTH 2 WITHOUT : 113ms
	# DEPTH 2 WITH : 776ms
	# DEPTH 4 : 17064ms
	print(score)
	print(move)
	# print(gomoku.player_turn)
