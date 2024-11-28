import sys
import os
import re
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.line_utils import get_line_horizontal, get_line_vertical, get_line_diagonal_1, get_line_diagonal_2
from algorithms.GomokuRegex import GomokuRegex
from LittleGomoku import LittleGomoku

def is_pertinent_line(line: str, player_pos: int):
	gomokuRegex = GomokuRegex()
	white_streaks = re.search(gomokuRegex.white_streaks, line)
	if white_streaks:
		return True
	black_streaks = re.search(gomokuRegex.black_streaks, line)
	if black_streaks:
		return True

	# print(f"'{remove_player_line}'", player_pos)
	remove_player_line = line[:player_pos] + " " + line[player_pos + 1:]
	captured = re.search(gomokuRegex.capture, remove_player_line)
	if captured:
		return True
	return False

def useful_alignment_placement(littleGomoku: LittleGomoku, i: int, j: int):
	line_horizontal, player_lh = get_line_horizontal(littleGomoku.board, i, j, stone=littleGomoku.player_turn, preshot=True)
	line_vertical, player_lv = get_line_vertical(littleGomoku.board, i, j, stone=littleGomoku.player_turn, preshot=True)
	line_diagonal_1, player_ld1 = get_line_diagonal_1(littleGomoku.board, i, j, stone=littleGomoku.player_turn, preshot=True)
	line_diagonal_2, player_ld2 = get_line_diagonal_2(littleGomoku.board, i, j, stone=littleGomoku.player_turn, preshot=True)

	# print("=" * 20)
	# print(f"'{line_horizontal}'")
	# print(f"'{line_vertical}'")
	# print(f"'{line_diagonal_1}'")
	# print(f"'{line_diagonal_2}'")
	return is_pertinent_line(line_horizontal, player_lh) or is_pertinent_line(line_vertical, player_lv) or is_pertinent_line(line_diagonal_1, player_ld1) or is_pertinent_line(line_diagonal_2, player_ld2)




def _prune_action(board: list[list[str]], actions: list[tuple[int]], stone: str = None):
	new_actions = []
	for action in actions:
		if useful_alignment_placement(board=board, i=action[0], j=action[1]):
			print(f"HERE : {action[0]}, {action[1]}")
			new_actions.append(action)
	# if len(new_actions) == 0 and len(actions) >= 1:
	# 	new_actions.append(actions[0])
	return new_actions

def prune_action(littleGomoku: LittleGomoku, actions: list[tuple[int]]):
	new_actions = []
	for action in actions:
		if useful_alignment_placement(littleGomoku=littleGomoku, i=action[0], j=action[1]):
			new_actions.append(action)
	if len(new_actions) == 0 and len(actions) >= 1:
		new_actions.append(actions[0])
	return new_actions

if __name__ == "__main__":
	from Gomoku import Gomoku
	from algorithms.gomoku_algorithm import super_minimax, minimax
	from utils.little_gomoku_utils import convert_to_little_gomoku
	from utils.MeasureTime import MeasureTime
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

	gomoku.place_stone("H6", "W")
	gomoku.switch_player_turn()
	gomoku.place_stone("J9", "B")
	gomoku.switch_player_turn()

	mt = MeasureTime(True)
	littleGomoku = convert_to_little_gomoku(gomoku=gomoku)

	# score, move = super_minimax(littleGomoku, MAX_DEPTH=8)
	# print(f"Score : {score} | Move {move} | Total node : {littleGomoku.minimax_node}")
	# mt.stop()

	littleGomoku.paint_actions(prune_action(littleGomoku, littleGomoku.get_actions()), live_visualisation=True)
	print(littleGomoku)



if __name__ == "__main__2":
		from LittleGomoku import LittleGomoku
		from Gomoku import Gomoku
		from utils.little_gomoku_utils import convert_to_little_gomoku
		gomoku = Gomoku(ia_against_ia=False)
		gomoku.read_a_game(41, -1, live_visualisation=False, live_speed=0.1)
		littleGomoku1 = convert_to_little_gomoku(gomoku)
		littleGomoku2 = copy.deepcopy(littleGomoku1)

		print(littleGomoku1.paint_actions(littleGomoku1.get_actions()))
		print(littleGomoku1)
		littleGomoku2.paint_actions(_prune_action(littleGomoku2.board, littleGomoku2.get_actions(), littleGomoku2.player_turn))
		littleGomoku2.paint_actions(prune_action(littleGomoku2, littleGomoku2.get_actions(), littleGomoku2.player_turn))
		print(littleGomoku2)
		# print(gomoku)


if __name__ == "__main__2":
	import sys
	import os
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	from Gomoku import Gomoku
	from utils.MeasureTime import MeasureTime
	from utils.little_gomoku_utils import convert_to_little_gomoku
	# from LittleGomoku import LittleGomoku
	import time
	import copy

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

	littleGomoku1 = convert_to_little_gomoku(gomoku=gomoku)
	littleGomoku2 = copy.deepcopy(littleGomoku1)

	i, j = 6, 5
	i, j = 5, 10

	# get_line_horizontal(gomoku.board, i, j)
	# get_line_vertical(gomoku.board, i, j)
	# get_line_diagonal_1(gomoku.board, i, j)
	# get_line_diagonal_2(gomoku.board, i, j)
	# useful_alignment_placement(gomoku.board, i, j)
	littleGomoku1.paint_actions(littleGomoku1.super_get_actions())
	print(littleGomoku1)
	# print(prune_action(littleGomoku2.board, littleGomoku2.get_actions()))
	littleGomoku2.paint_actions(prune_action(littleGomoku2, littleGomoku2.super_get_actions(), littleGomoku2.player_turn))
	print(littleGomoku2)
