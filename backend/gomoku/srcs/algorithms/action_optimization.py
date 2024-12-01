import sys
import os
import re
import copy
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.line_utils import get_line_horizontal, get_line_vertical, get_line_diagonal_1, get_line_diagonal_2
from algorithms.count_alignment import type_of_alignment
from algorithms.handle_alignment import adjust_list
from algorithms.GomokuRegex import GomokuRegex
from algorithms.gomoku_heuristic_function import game_state
from LittleGomoku import LittleGomoku
from utils.little_gomoku_utils import is_useful_placement

def get_score_from_action(gomoku: LittleGomoku, all_streaks: dict):
	S_FIVE_ALIGNED = 15000
	S_FREE_FOUR = 3000
	S_FOUR_ALIGNED = 1500
	S_FREE_THREE = 1000
	S_THREE_ALIGNED = 100


	# # == PAIRS ==
	pairs = {
		'0': 0,
		'1': 50,
		'2': 200,
		'3': 400,
		'4': 2500,
		'5': 15000
	}

	score_white = 0
	score_black = 0

	########################################
	# FIVE ALIGNED
	########################################
	score_black += all_streaks['five_aligned_black'] * S_FIVE_ALIGNED
	score_white += all_streaks['five_aligned_white'] * S_FIVE_ALIGNED

	########################################
	# FREE FOUR
	########################################
	score_black += all_streaks['free_four_black'] * S_FREE_FOUR
	score_white += all_streaks['free_four_white'] * S_FREE_FOUR

	########################################
	# FOUR ALIGNED
	########################################
	score_black += all_streaks['four_aligned_black'] * S_FOUR_ALIGNED
	score_white += all_streaks['four_aligned_white'] * S_FOUR_ALIGNED

	########################################
	# FREE THREE
	########################################
	score_black += all_streaks['free_three_black'] * S_FREE_THREE
	score_white += all_streaks['free_three_white'] * S_FREE_THREE

	########################################
	# THREE ALIGNED
	########################################
	score_black += all_streaks['three_aligned_black'] * S_THREE_ALIGNED
	score_white += all_streaks['three_aligned_white'] * S_THREE_ALIGNED

	########################################
	# PAIRS CATCHED
	########################################

	if gomoku.settings.allowed_win_by_capture == True:
		if all_streaks['black_capture'] > 5:
			score_black += pairs['5']
		else:
			score_black += pairs[f"{all_streaks['black_capture']}"]
		if all_streaks['white_capture'] > 5:
			score_white += pairs['5']
		else:
			score_white += pairs[f"{all_streaks['white_capture']}"]

	if gomoku.maximizing_player == "B":
		return score_black - score_white
	else:
		return score_white - score_black

def evaluate_pertinent(gomoku: LittleGomoku, black_streaks: list, white_streaks: list, stones_catchable: list):
	gomokuRegex = GomokuRegex()
	if black_streaks == [] and white_streaks == [] and stones_catchable == []:
		return None
	all_streaks = {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,

		'black_capture': 0,
		'white_capture': 0,
	}

	if white_streaks:
		white_streaks = adjust_list(white_streaks)
		for streak in white_streaks:
			if (len(streak)) < 5:
				continue
			type_align, number = type_of_alignment(streak, 'W')
			if type_align == 'free':
				if number == 3:
					all_streaks['free_three_white'] += 1
				elif number == 4:
					all_streaks['free_four_white'] += 1
			elif type_align == 'align':
				if number == 3:
					all_streaks['three_aligned_white'] += 1
				elif number == 4:
					all_streaks['four_aligned_white'] += 1
				elif number == 5:
					all_streaks['five_aligned_white'] += 1

	if black_streaks:
		black_streaks = adjust_list(black_streaks)
		for streak in black_streaks:
			if (len(streak)) < 5:
				continue
			# print(streak)
			type_align, number = type_of_alignment(streak, 'B')
			if type_align == 'free':
				if number == 3:
					all_streaks['free_three_black'] += 1
				elif number == 4:
					all_streaks['free_four_black'] += 1
			elif type_align == 'align':
				if number == 3:
					all_streaks['three_aligned_black'] += 1
				elif number == 4:
					all_streaks['four_aligned_black'] += 1
				elif number == 5:
					all_streaks['five_aligned_black'] += 1
	if stones_catchable:
		for stone in stones_catchable:
			if stone.count("W") == 2:
				all_streaks['black_capture']
			if stone.count("B") == 2:
				all_streaks['white_capture']

	return get_score_from_action(gomoku, all_streaks)


def get_line_pertinent(gomoku: LittleGomoku, line: str, player_pos: int):
	gomokuRegex = GomokuRegex()

	remove_player_line = line[:player_pos] + " " + line[player_pos + 1:]

	white_streaks = re.findall(gomokuRegex.white_streaks, line)
	if white_streaks != []:
		for streak in white_streaks:
			if (len(streak)) < 5:
				continue
			if type_of_alignment(streak, 'W')[0] != 'invalid':
				return True
	black_streaks = re.findall(gomokuRegex.black_streaks, line)
	if black_streaks != []:
		for streak in black_streaks:
			if (len(streak)) < 5:
				continue
			if type_of_alignment(streak, 'B')[0] != 'invalid':
				return True
	captured = re.findall(gomokuRegex.capture, remove_player_line)
	if captured != []:
		return True
	return False

	return white_streaks != None or black_streaks != None or captured != None
	# print(white_streaks, black_streaks, captured)
	return evaluate_pertinent(
		gomoku=gomoku,
		black_streaks=black_streaks,
		white_streaks=white_streaks,
		stones_catchable=captured)

def useful_alignment_placement(littleGomoku: LittleGomoku, i: int, j: int, stone: str = None, preshot: bool = True):
	if stone == None:
		stone = littleGomoku.player_turn

	line_horizontal, player_lh = get_line_horizontal(littleGomoku.board, i, j, stone=stone, preshot=preshot)
	line_vertical, player_lv = get_line_vertical(littleGomoku.board, i, j, stone=stone, preshot=preshot)
	line_diagonal_1, player_ld1 = get_line_diagonal_1(littleGomoku.board, i, j, stone=stone, preshot=preshot)
	line_diagonal_2, player_ld2 = get_line_diagonal_2(littleGomoku.board, i, j, stone=stone, preshot=preshot)

	# print(f"'{line_horizontal}'")
	# print(f"'{line_vertical}'")
	# print(f"'{line_diagonal_1}'")
	# print(f"'{line_diagonal_2}'")
	all_pertinent = [
		get_line_pertinent(littleGomoku, line_horizontal, player_lh),
		get_line_pertinent(littleGomoku, line_vertical, player_lv),
		get_line_pertinent(littleGomoku, line_diagonal_1, player_ld1),
		get_line_pertinent(littleGomoku, line_diagonal_2, player_ld2)
	]
	return any(all_pertinent)

	# print("=" * 20)
	# print(f"'{line_horizontal}'")
	# print(f"'{line_vertical}'")
	# print(f"'{line_diagonal_1}'")
	# print(f"'{line_diagonal_2}'")
	# return is_pertinent_line(line_horizontal, player_lh) or is_pertinent_line(line_vertical, player_lv) or is_pertinent_line(line_diagonal_1, player_ld1) or is_pertinent_line(line_diagonal_2, player_ld2)



def prune_action(littleGomoku: LittleGomoku, actions: list[tuple[int]]):
	sort_new_actions = []
	for action in actions:

		if useful_alignment_placement(littleGomoku=littleGomoku, i=action[0], j=action[1]) == True:
			# print(f"Useful : {action[0]}, {action[1]}")
			try:
				count_same, count_different = is_useful_placement(littleGomoku.board, action[0], action[1], littleGomoku.player_turn)
				gs = littleGomoku.do_simulation(action)
				sort_new_actions.append((action, game_state(littleGomoku) + (count_same + count_different) * 0.1))
				littleGomoku.undo_simulation(gs)
			except:
				pass
	if len(sort_new_actions) == 0 and len(actions) >= 1:
		for action in actions:
			try:
				gs = littleGomoku.do_simulation(action)
				sort_new_actions.append((action, game_state(littleGomoku)))
				littleGomoku.undo_simulation(gs)
			except:
				pass
		max_action = len(sort_new_actions) if len(sort_new_actions) < 5 else 5
		sort_new_actions = sort_new_actions[:max_action]

	list_orientation = False if littleGomoku.player_turn == littleGomoku.minimizing_player else True
	sort_new_actions.sort(key=lambda x: x[-1], reverse=list_orientation)
	return [item[0] for item in sort_new_actions]

if __name__ == "__main__":
	from Gomoku import Gomoku
	from algorithms.gomoku_algorithm import super_minimax, minimax
	from utils.little_gomoku_utils import convert_to_little_gomoku
	from utils.MeasureTime import MeasureTime
	from utils.gomoku_utils import convert_xy_to_coordinate, convert_coordinate_to_xy

	go_simulate = Gomoku(main_player="B", ia_against_ia=True, IA_MAX_DEPTH=2, IA_AGAINST_IA_MAX_DEPTH=4)
	# go_simulate.read_a_game(61, -6, live_visualisation=False, live_speed=0.1)
	go_simulate.read_a_game(72, 10, live_visualisation=False, live_speed=0.1, skip_error=False)

	littleGomoku = convert_to_little_gomoku(gomoku=go_simulate)

	if True:
		mt = MeasureTime(True)
		score, move = super_minimax(littleGomoku, MAX_DEPTH=4, TIMEOUT=8)
		print(f"Score : {score} | Move {move} | Total node : {littleGomoku.minimax_node}")
		littleGomoku.board[move[0]][move[1]] = 'XX'
		mt.stop()

	# j, i = convert_coordinate_to_xy("K11")
	# littleGomoku.simulate_action()
	# print(game_state(littleGomoku))
	# print(littleGomoku.black_capture)
	# print(littleGomoku.white_capture)
	# print(useful_alignment_placement(littleGomoku, 12, 8))
	# littleGomoku.paint_actions(prune_action(littleGomoku, littleGomoku.get_actions()), live_visualisation=True)
	# littleGomoku.paint_actions(littleGomoku.ultimate_get_actions(), live_visualisation=True)
	# print(littleGomoku.ultimate_get_actions())

	print(go_simulate)
	# print(game_state(littleGomoku))
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)

	# go_simulate.play()

if __name__ == "__main__2":
	from Gomoku import Gomoku
	from algorithms.gomoku_algorithm import super_minimax, minimax
	from utils.little_gomoku_utils import convert_to_little_gomoku
	from utils.MeasureTime import MeasureTime
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	# gomoku.place_stone("H7", "W")
	# gomoku.place_stone("J3", "B")
	# gomoku.place_stone("H8", "W")
	# gomoku.place_stone("J8", "B")
	# gomoku.place_stone("H9", "W")
	# gomoku.place_stone("J10", "B")
	# gomoku.place_stone("R17", "W")
	# gomoku.place_stone("R18", "B")
	# gomoku.switch_player_turn()

	# gomoku.place_stone("H6", "W")
	# gomoku.switch_player_turn()
	# gomoku.place_stone("J9", "B")
	# gomoku.switch_player_turn()
	print(gomoku.player_turn)
	print(gomoku.maximizing_player)
	print(gomoku.minimizing_player)

	mt = MeasureTime(True)
	littleGomoku = convert_to_little_gomoku(gomoku=gomoku)

	if True:
		score, move = super_minimax(littleGomoku, MAX_DEPTH=6)
		littleGomoku.board[move[0]][move[1]] = 'XX'
		print(f"Score : {score} | Move {move} | Total node : {littleGomoku.minimax_node}")
	mt.stop()

	# littleGomoku.paint_actions(littleGomoku.get_actions(), live_visualisation=True)
	# print(useful_alignment_placement(littleGomoku, 5, 8))

	# littleGomoku.paint_actions(prune_action(littleGomoku, littleGomoku.get_actions()), live_visualisation=False)
	print(littleGomoku)


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
