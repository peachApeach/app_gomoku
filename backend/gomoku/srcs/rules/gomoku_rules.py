def switch_opponent(string: str) -> str:
	r_str = ""
	for c in string:
		if c == "W":
			r_str += "B"
		elif c == "B":
			r_str += "W"
		else:
			r_str += c
	return r_str

def pair_can_be_capture(board: list[list[str]], i, j, stone) -> list[list[tuple[int]]]:
	possibility = ("WBBW", "BWWB")
	captured = []
	try: # F
		if stone + "".join([board[i][j + k] for k in range(1, 4)]) in possibility:
			captured.append([(i, j + 1), (i, j + 2)])
	except:
		pass
	try: # I
		if stone + "".join([board[i][j - k] for k in range(1, 4)]) in possibility:
			captured.append([(i, j - 1), (i, j - 2)])
	except:
		pass
	try: # G
		if stone + "".join([board[i + k][j] for k in range(1, 4)]) in possibility:
			captured.append([(i + 1, j), (i + 2, j)])
	except:
		pass
	try: # E
		if stone + "".join([board[i - k][j] for k in range(1, 4)]) in possibility:
			captured.append([(i - 1, j), (i - 2, j)])
	except:
		pass
	try: # A
		if stone + "".join([board[i - k][j - k] for k in range(1, 4)]) in possibility:
			captured.append([(i - 1, j - 1), (i - 2, j - 2)])
	except:
		pass
	try: # D
		if stone + "".join([board[i + k][j + k] for k in range(1, 4)]) in possibility:
			captured.append([(i + 1, j + 1), (i + 2, j + 2)])
	except:
		pass
	try: # C
		if stone + "".join([board[i - k][j + k] for k in range(1, 4)]) in possibility:
			captured.append([(i - 1, j + 1), (i - 2, j + 2)])
	except:
		pass
	try: # H
		if stone + "".join([board[i + k][j - k] for k in range(1, 4)]) in possibility:
			captured.append([(i + 1, j - 1), (i + 2, j - 2)])
	except:
		pass
	return captured

# board = [
# 	[" ", "C", " ", " ", " ", " ", " ", " "],
# 	["W", " ", " ", "W", " ", " ", "W", " "],
# 	[" ", "A", " ", "E", " ", "C", " ", " "],
# 	[" ", " ", "A", "E", "C", " ", " ", " "],
# 	["W", "I", "I", "W", "F", "F", "W", " "],
# 	[" ", " ", "H", "G", "D", " ", " ", " "],
# 	[" ", "H", " ", "G", " ", "D", " ", " "],
# 	["W", " ", " ", "W", " ", " ", "W", " "],
# 	[" ", " ", " ", " ", " ", " ", " ", " "],
# ]

def is_free_three(board: list[list[str]], i, j, stone):
	"""
	Les free_three possibles :
	'  BBB ' => ' BBBB '
	' B BB ' => ' BBBB '
	' BB B ' => ' BBBB '
	' BBB  ' => ' BBBB '
	"""
	count = 0
	if stone == 'B':
		possibility = ("  BBB ", " BBB  ", " B BB ", " BB B ")
		large_double_three = "  BBB  "
	elif stone == 'W':
		possibility = ("  WWW ", " WWW  ", " W WW ", " WW W ")
		large_double_three = "  WWW  "
	else:
		return count
	try: # F
		if "".join([board[i][j + k] for k in range(0, 6)]) in possibility:
			count += 1
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(0, 6)]) in possibility:
			count += 1
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(0, 6)]) in possibility:
			count += 1
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(0, 6)]) in possibility:
			count += 1
	except:
		pass
	return count


def check_alignment(row: list[str], stone: str, stone_count: int) -> bool:
	return row.count(stone) == stone_count and row.count(" ") == len(row) - stone_count
	pass

def is_three_aligned(board: list[list[str]], i, j, stone):
	count = 0

	try: # F
		if check_alignment("".join([board[i][j + k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # I
		if check_alignment("".join([board[i][j - k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # G
		if check_alignment("".join([board[i + k][j] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # E
		if check_alignment("".join([board[i - k][j] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # A
		if check_alignment("".join([board[i - k][j - k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # D
		if check_alignment("".join([board[i + k][j + k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # C
		if check_alignment("".join([board[i - k][j + k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # H
		if check_alignment("".join([board[i + k][j - k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	return count










def is_free_three_no_doublons(board: list[list[str]], i, j, stone):
	"""
	Les free_three possibles :
	'  BBB ' => ' BBBB '
	' B BB ' => ' BBBB '
	' BB B ' => ' BBBB '
	' BBB  ' => ' BBBB '
	"""
	count = 0
	if stone == 'B':
		possibility = ("  BBB ", " BBB  ", " B BB ", " BB B ")
		large_double_three = "  BBB  "
	elif stone == 'W':
		possibility = ("  WWW ", " WWW  ", " W WW ", " WW W ")
		large_double_three = "  WWW  "
	else:
		return count
	try: # F
		# print(f"{i}:{j}" ,"{" ,"".join([board[i][j + k] for k in range(0, 6)]), "}")
		# raise Exception
		if "".join([board[i][j + k] for k in range(0, 6)]) in possibility:
			count += 1
			if "".join([board[i][j + k] for k in range(0, 7)]) == large_double_three:
				count -= 1
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(0, 6)]) in possibility:
			count += 1
			if "".join([board[i + k][j] for k in range(0, 7)]) == large_double_three:
				count -= 1
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(0, 6)]) in possibility:
			count += 1
			if "".join([board[i + k][j + k] for k in range(0, 7)]) == large_double_three:
				count -= 1
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(0, 6)]) in possibility:
			count += 1
			if "".join([board[i + k][j - k] for k in range(0, 7)]) == large_double_three:
				count -= 1
	except:
		pass
	return count


def count_free_three(board: list[list[str]], stone: str):
	count = 0
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == " ":
				count += is_free_three_no_doublons(board, i, j, stone)
	return count


def count_three_aligned(board: list[list[str]], stone: str):
	count = 0
	opponent_stone = switch_opponent(stone)
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == opponent_stone:
				count += is_three_aligned(board, i, j, stone)
	return count

def count_all_three(board: list[list[str]], stone: str):
	free_three = count_free_three(board, stone)
	three_aligned = count_three_aligned(board, stone)
	return {
		'free_three': free_three,
		'three_aligned': three_aligned
	}

def is_creating_db_free_three(board: list[list[str]], i_stone: int, j_stone: int, stone: str):
	before_count = 0
	after_count = 0
	# top_left = board[i_stone - 3][j_stone - 3]
	# bottom_right = board[i_stone + 3][j_stone + 3]
	# print(top_left)
	# print(bottom_right)
	i_min = i_stone - 4 if i_stone - 4 >= 0 else 0
	i_max = i_stone + 5 if i_stone + 5 < len(board) else len(board)

	j_min = j_stone - 4 if j_stone - 4 >= 0 else 0
	j_max = j_stone + 5 if j_stone + 5 < len(board[i_min]) else len(board[i_min])


	for i in range(i_min, i_max):
		for j in range(j_min, j_max):
			if i < 0 or j < 0 or i >= len(board) or j >= len(board[i]):
				continue
			if board[i][j] == " ":
				before_count += is_free_three_no_doublons(board, i, j, stone)

	board[i_stone][j_stone] = stone
	for i in range(i_min, i_max):
		for j in range(j_min, j_max):
			if i < 0 or j < 0 or i >= len(board) or j >= len(board[i]):
				continue
			if board[i][j] == " ":
				after_count += is_free_three_no_doublons(board, i, j, stone)
	board[i_stone][j_stone] = ' '


	# print(f"BEFORE COUNT => {before_count}")
	# print(f"AFTER COUNT => {after_count}")
	return after_count - 2 >= before_count

if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone("C5", "W")
	gomoku.place_stone("D6", "B")

	gomoku.place_stone("C8", "B")
	gomoku.place_stone("D8", "B")

	gomoku.place_stone("C11", "B")
	gomoku.place_stone("D10", "B")

	gomoku.place_stone("F10", "B")
	gomoku.place_stone("F11", "B")

	gomoku.place_stone("H10", "B")
	gomoku.place_stone("I11", "W")

	gomoku.place_stone("H8", "B")
	gomoku.place_stone("I8", "B")

	gomoku.place_stone("H6", "B")
	gomoku.place_stone("I5", "B")

	gomoku.place_stone("F5", "B")
	gomoku.place_stone("F6", "B")



	# gomoku.place_stone("C11", "W")
	# gomoku.place_stone("F9", "B")
	# gomoku.place_stone("F10", "B")

	# gomoku.place_stone("I11", "W")
	# with pytest.raises(PlacementError):
	# 	gomoku.place_stone("F8", "B")
	print(is_creating_db_free_three(gomoku.board, 5, 7, "B"))
	print(gomoku)
	exit(1)

def remove_pair_capture(board: list[list[str]]) -> dict | None:
	for i in range(len(board)):
		for j in range(len(board[i])):
			value = pair_can_be_capture(board, i, j)
			if value != []:
				return {'stone_attack': board[i][j], 'coordinate_to_remove': value}
	return None


def main0():
	from Gomoku import Gomoku
	gomoku = Gomoku()
	# HORIZONTAL
	t = 3
	for i in range(9):
		if i % 2 == 0:
			gomoku.place_stone(f"C{t}")
			t += 1
		else:
			gomoku.place_stone(f"I{i + 1}")

	# VERTICAL
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D5", "B")
	gomoku.place_stone(f"E5", "B")
	gomoku.place_stone(f"F5", "B")
	gomoku.place_stone(f"G5", "B")
	for i in range(6, 10):
		gomoku.place_stone(f"I{i}", "W")

	# DIAGONAL
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D6", "B")
	gomoku.place_stone(f"E7", "B")
	gomoku.place_stone(f"F8", "B")
	gomoku.place_stone(f"G9", "B")
	for i in range(6, 10):
		gomoku.place_stone(f"I{i}", "W")

	# TIE
	for i in range(len(gomoku.board)):
		for j in range(len(gomoku.board[i])):
			gomoku.board[i][j] = 'B'

def main1():
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D5", "W")
	gomoku.place_stone(f"E5", "W")
	print(remove_pair_capture(gomoku.board))
	gomoku.place_stone(f"F5", "B")
	print(remove_pair_capture(gomoku.board))

def main_creating_double_three():
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D6", "B")
	gomoku.place_stone(f"F9", "B")
	gomoku.place_stone(f"F10", "B")
	# print(is_creating_double_three(gomoku.board, 5, 7, "B"))

	gomoku.place_stone(f"G9", "B")
	gomoku.place_stone(f"H10", "B")
	# gomoku.place_stone(f"I11", "B")


	# gomoku.place_stone(f"F8", "B")
	print(count_free_three(gomoku.board, "B"))
	gomoku.place_stone(f"F8", "B")
	print(count_free_three(gomoku.board, "B"))
	# print(is_creating_double_three(gomoku.board, 5, 7, "B"))
	print(gomoku)
	# print(remove_pair_capture(gomoku.board))

if __name__ == "__main__":
	# print(switch_opponent("WBBW  B"))
	main_creating_double_three()
	# stri = "BB B "
	# print(stri.count("B"))
	# print(stri.count(" "))
	# test2()


	# print(gomoku)
	# print(terminate_state(gomoku.board))
	pass
