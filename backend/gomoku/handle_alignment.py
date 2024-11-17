import re
from gomoku_rules import switch_opponent

def type_of_alignment(row: list[str], stone: str):
	opponent_stone = switch_opponent(stone)
	opponent_count = row.count(opponent_stone)
	if opponent_count > 1:
		return 'invalid', 0
	if opponent_count == 1:
		if row[0] != opponent_stone and row[-1] != opponent_stone:
			return 'invalid', 0
	if row[0] == " " and row[-1] == " ":
		return 'free', row.count(stone)
	else:
		return 'align', row.count(stone)

def alignment_streaks(line: str):
	all_streaks = {
		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}

	white_streaks = re.findall(r"(\s*[W]{2,}\s?[W]*\s?)", line)
	if white_streaks:
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

	black_streaks = re.findall(r"(\s*[B]{2,}\s?[B]*\s?)", line)
	if black_streaks:
		for streak in black_streaks:
			if (len(streak)) < 5:
				continue
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

if __name__ == "__main__":
	from Colors import *
	from MeasureTime import MeasureTime
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

	gomoku.place_stone("S19", "B")
	print(gomoku)
	count_all_alignment(gomoku.board, 18, 18)
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
