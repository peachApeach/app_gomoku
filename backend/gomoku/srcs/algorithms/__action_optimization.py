import sys
import os
import re
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LittleGomoku import LittleGomoku
from algorithms.gomoku_heuristic_function import game_state
from utils.little_gomoku_utils import is_useful_placement


def update_action_efficient(all_actions: list[tuple[int]], pos: int, gomoku: LittleGomoku, action: tuple[int]):
	# import time
	# time.sleep(1)
	i = action[0]
	j = action[1]
	before_game_state = game_state(gomoku)
	try:
		gs = gomoku.do_simulation(action)
		next_game_state = game_state(gomoku)
		gomoku.undo_simulation(gs)
		if before_game_state == next_game_state:
			return
		all_actions[pos] = (action, next_game_state + (count_same) * 2 + count_different)
		return
	except:
		return

if __name__ == "__main__":
	from Gomoku import Gomoku
	from utils.little_gomoku_utils import convert_to_little_gomoku
	from utils.MeasureTime import MeasureTime

	# gomoku = Gomoku(main_player="B", ia_against_ia=True, IA_MAX_DEPTH=2, IA_AGAINST_IA_MAX_DEPTH=4)

	# gomoku.read_a_game(43, -14, live_visualisation=False, live_speed=0.1)

	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R17", "W")
	gomoku.place_stone("R18", "B")
	gomoku.switch_player_turn()

	littleGomoku = convert_to_little_gomoku(gomoku=gomoku)
	# mt = MeasureTime(start=True)

	# print(littleGomoku.ultimate_get_actions())
	littleGomoku.paint_actions(littleGomoku.ultimate_get_actions(), live_visualisation=True)
	print(littleGomoku)
