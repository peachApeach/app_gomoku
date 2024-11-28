def get_line_horizontal(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""
	min_j = params_j - radius
	if min_j < 0:
		min_j = 0
	max_j = params_j + (radius + 1)
	if max_j > len(board[params_i]):
		max_j = len(board[params_i])

	for j in range(min_j, max_j):
		if j == params_j:
			board[params_i][j] = "XX"
		else:
			board[params_i][j] = "??"
		# line += board[params_i][j]
	# return alignment_streaks(line)

def get_line_vertical(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""
	min_i = params_i - radius
	if min_i < 0:
		min_i = 0
	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	for i in range(min_i, max_i):
		if i == params_i:
			board[i][params_j] = "XX"
		else:
			board[i][params_j] = "??"
	# 	line += board[params_i][j]
	# return alignment_streaks(line)

def get_line_diagonal_1(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""


	i_radius = 0
	min_i = params_i
	min_j = params_j

	while i_radius < radius and min_i > 0 and min_j > 0:
		min_i -= 1
		min_j -= 1
		i_radius += 1


	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	max_j = params_j + (radius + 1)
	if max_j > len(board[params_i]):
		max_j = len(board[params_i])

	for i, j in zip(range(min_i, max_i), range(min_j, max_j)):
		if i == params_i and j == params_j:
			board[i][j] = "XX"
		else:
			board[i][j] = "??"
	# return alignment_streaks(line)

def get_line_diagonal_2(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""

	i_radius = 0
	min_i = params_i
	min_j = params_j

	while i_radius < radius and min_i > 0 and min_j < len(board[params_i]) - 1:
		min_i -= 1
		min_j += 1
		i_radius += 1

	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	max_j = params_j - radius
	if max_j < 0:
		max_j = 0

	for i, j in zip(range(min_i, max_i), range(min_j, max_j - 1, -1)):
		if i == params_i and j == params_j:
			board[i][j] = "XX"
		else:
			board[i][j] = "??"


	# while i < len(board) and j >= 0:
	# 	line += board[params_i][j]
	# 	i += 1
	# 	j -= 1
	# return alignment_streaks(line)

def useful_alignment_placement(board: list[list[str]], i: int, j: int):
	dict_horizontal = get_line_horizontal(board, i)
	dict_vertical = get_line_vertical(board, j)
	tmp_i = i
	tmp_j = j

	while tmp_i > 0 and tmp_j > 0:
		tmp_i -= 1
		tmp_j -= 1
	dict_diagonal_1 = get_line_diagonal_1(board, tmp_i, tmp_j)

	tmp_i = i
	tmp_j = j
	while tmp_i > 0 and tmp_j < len(board[0]) - 1:
		tmp_i -= 1
		tmp_j += 1
	dict_diagonal_2 = get_line_diagonal_2(board, tmp_i, tmp_j)


def prune_action(board: list[list[str]], actions: list[tuple]):
	pass

if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	from Gomoku import Gomoku
	from utils.MeasureTime import MeasureTime
	from utils.little_gomoku_utils import convert_to_little_gomoku
	# from LittleGomoku import LittleGomoku
	import time

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
	# littleGomoku.paint_actions(littleGomoku.super_get_actions())

	i, j = 6, 5
	i, j = 18, 0

	get_line_horizontal(gomoku.board, i, j)
	get_line_vertical(gomoku.board, i, j)
	get_line_diagonal_1(gomoku.board, i, j)
	get_line_diagonal_2(gomoku.board, i, j)
	print(littleGomoku)
