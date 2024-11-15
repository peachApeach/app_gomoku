import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
from gomoku_algorithm import minimax, minimax2
from little_gomoku_utils import convert_to_little_gomoku
from MeasureTime import MeasureTime

if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.read_a_game(9, -13, live_visualisation=False, live_speed=0.5)
	print(gomoku)
	littleGomoku = convert_to_little_gomoku(gomoku)
	mt = MeasureTime(start=True)
	score, move = minimax2(gomoku=littleGomoku, MAX_DEPTH=2)
	mt.stop()
	# DEPTH 2 WITHOUT : 113ms
	# DEPTH 2 WITH : 776ms
	# DEPTH 4 WITHOUT ALL: 17064ms -15090 | (5, 11)
	# DEPTH 4 WITH BREAK: 12064ms -13110 | (4, 8)
	# DEPTH 4 WITH DANGEROUS LIMIT: 12064ms -15090 | (5, 11)
	print(score)
	print(move)
	# print(gomoku.player_turn)
