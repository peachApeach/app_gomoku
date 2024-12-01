import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
from utils.Colors import *
from utils.little_gomoku_utils import convert_to_little_gomoku

if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R18", "W")
	gomoku.place_stone("C16", "B")

	lg = convert_to_little_gomoku(gomoku)

	for action in lg.ultimate_get_actions():
		print(lg.simulate_action(action))

	lg.paint_actions(lg.ultimate_get_actions(), live_visualisation=True)
	# print(gomoku)
