import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rules.gomoku_rules import switch_opponent
from algorithms.count_alignment import type_of_alignment
from algorithms.StreaksRegex import StreaksRegex
from algorithms.line_utils import get_line_horizontal, get_line_vertical, get_line_diagonal_1, get_line_diagonal_2

def adjust_list(lst: list[str]):
	for i in range(1, len(lst)):
		if len(lst[i - 1]) == 0:
			continue
		if lst[i - 1][-1] == " ":
			lst[i] = " " + lst[i]
	return lst

def alignment_streaks(line: str):
	streaksRegex = StreaksRegex()

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
	}

	white_streaks = re.findall(streaksRegex.white_pattern, line)
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

	black_streaks = re.findall(streaksRegex.black_pattern, line)
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
	return all_streaks

def count_horizontal(board: list[list[str]], i: int):
	line = ""
	for j in range(len(board[i])):
		line += board[i][j]
	return alignment_streaks(line)

def count_vertical(board: list[list[str]], j: int):
	line = ""
	for i in range(len(board)):
		line += board[i][j]
	return alignment_streaks(line)

def count_diagonal_1(board: list[list[str]], i: int, j: int):
	line = ""
	while i < len(board) and j < len(board[i]):
		line += board[i][j]
		i += 1
		j += 1
	return alignment_streaks(line)

def count_diagonal_2(board: list[list[str]], i: int, j: int):
	line = ""
	while i < len(board) and j >= 0:
		line += board[i][j]
		i += 1
		j -= 1
	return alignment_streaks(line)

def count_all_alignment(board: list[list[str]], i: int, j: int):

	# dict_horizontal = alignment_streaks(get_line_horizontal(board, i, j, 7))
	# dict_vertical = alignment_streaks(get_line_vertical(board, i, j, 7))
	# dict_diagonal_1 = alignment_streaks(get_line_diagonal_1(board, i, j, 7))
	# dict_diagonal_2 = alignment_streaks(get_line_diagonal_2(board, i, j, 7))


	dict_horizontal = count_horizontal(board, i)
	dict_vertical = count_vertical(board, j)
	tmp_i = i
	tmp_j = j

	while tmp_i > 0 and tmp_j > 0:
		tmp_i -= 1
		tmp_j -= 1
	dict_diagonal_1 = count_diagonal_1(board, tmp_i, tmp_j)

	tmp_i = i
	tmp_j = j
	while tmp_i > 0 and tmp_j < len(board[0]) - 1:
		tmp_i -= 1
		tmp_j += 1
	dict_diagonal_2 = count_diagonal_2(board, tmp_i, tmp_j)
	return {
		k:
		dict_horizontal.get(k, 0)
		+ dict_vertical.get(k, 0)
		+ dict_diagonal_1.get(k, 0)
		+ dict_diagonal_2.get(k, 0)
		for k in set(dict_horizontal)
	}

def get_score_from_alignment(all_alignment: dict):
	S_FIVE_ALIGNED = 15000
	S_FREE_FOUR = 3000
	S_FOUR_ALIGNED = 1500
	S_FREE_THREE = 1000
	S_THREE_ALIGNED = 100


	score_white = 0
	score_black = 0

	########################################
	# FIVE ALIGNED
	########################################
	score_black += all_alignment['five_aligned_black'] * S_FIVE_ALIGNED
	score_white += all_alignment['five_aligned_white'] * S_FIVE_ALIGNED

	########################################
	# FREE FOUR
	########################################
	score_black += all_alignment['free_four_black'] * S_FREE_FOUR
	score_white += all_alignment['free_four_white'] * S_FREE_FOUR

	########################################
	# FOUR ALIGNED
	########################################
	score_black += all_alignment['four_aligned_black'] * S_FOUR_ALIGNED
	score_white += all_alignment['four_aligned_white'] * S_FOUR_ALIGNED

	########################################
	# FREE THREE
	########################################
	score_black += all_alignment['free_three_black'] * S_FREE_THREE
	score_white += all_alignment['free_three_white'] * S_FREE_THREE

	########################################
	# THREE ALIGNED
	########################################
	score_black += all_alignment['three_aligned_black'] * S_THREE_ALIGNED
	score_white += all_alignment['three_aligned_white'] * S_THREE_ALIGNED

	return score_black, score_white

if __name__ == "__main__":
	# print(alignment_streaks("  BBBBBWWWW BBBBB       "))
	# exit(1)


	from utils.Colors import *
	from utils.MeasureTime import MeasureTime
	from Gomoku import Gomoku

	gomoku = Gomoku()

	gomoku.place_stone("C5", "B")
	gomoku.place_stone("D6", "B")

	gomoku.place_stone("C8", "B")
	gomoku.place_stone("D8", "B")

	gomoku.place_stone("C11", "B")
	gomoku.place_stone("D10", "B")

	gomoku.place_stone("F10", "B")
	gomoku.place_stone("F11", "B")

	gomoku.place_stone("H10", "B")
	gomoku.place_stone("I11", "B")

	gomoku.place_stone("H8", "B")
	gomoku.place_stone("I8", "B")

	gomoku.place_stone("H6", "B")
	gomoku.place_stone("I5", "B")

	gomoku.place_stone("F5", "B")
	gomoku.place_stone("F6", "B")

	print(gomoku)
	# gomoku.place_stone("F8", "B", force=True)
	all_alignment = count_all_alignment(gomoku.board, 5, 7)
	print(all_alignment)
	print(get_score_from_alignment(all_alignment))
	print(gomoku)
	exit(1)

	i = 5
	j = 7

	mt = MeasureTime(start=True)
	print("BEFORE PLACEMENT")
	print(count_all_alignment(gomoku.board, i, j))
	print("AFTER PLACEMENT")
	gomoku.board[i][j] = "B"
	print(f'ALIGNMENT : {alignment_streaks("    BB B BB        ")}')
	print(count_all_alignment(gomoku.board, i, j))
	mt.stop()

	# i = 9
	# j = 3

	# i = 0
	# j = 0
	# count_all_alignment(gomoku.board, i, j)
	# print(gomoku)

	if True:
		mt = MeasureTime(start=True)
		iteration = 10000
		for _ in range(iteration):
			count_all_alignment(gomoku.board, i, j)

		print(f"{BHWHITE}Iteration : {YELLOWB}{BHBLACK} {iteration} {RESET} | ", end="")
		mt.stop()
	print(gomoku)

	line = "****BB***BB********"
	line = "    BB   BB        "
	line = "   BBB   BBB B     "
	line = "   BBB BBBB        "
	line = "   BBB  WWWW     BB B  WWWW"
	line = "BBB B  BBB BBBB        BBB        BB  BBBWBBB"
	# print(alignment_streaks(line))
	# print(alignment_streaks("   BBB WWWW        "))
	pass
