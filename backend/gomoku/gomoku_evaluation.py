
def win_from_pos(board: list[list[str]], i, j) -> bool:
	number_to_win = 5
	stone = board[i][j]
	if stone == ' ':
		return False
	# HORIZONTAL
	try:
		for k in range(number_to_win):
			if stone != board[i][j + k]:
				raise Exception
		return True
	except:
		pass

	# VERTICAL
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j]:
				raise Exception
		return True
	except:
		pass
	# DIAGONALE
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j + k]:
				raise Exception
		return True
	except:
		pass
	return False

def get_all_positions_pairs(board, i, j):
	possibility = ("WBBW", "BWWB")
	try: # F
		if "".join([board[i][j + k] for k in range(4)]) in possibility:
			return [(i, j + 1), (i, j + 2)]
	except:
		pass
	try: # I
		if "".join([board[i][j - k] for k in range(4)]) in possibility:
			return [(i, j - 1), (i, j - 2)]
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(4)]) in possibility:
			return [(i + 1, j), (i + 2, j)]
	except:
		pass
	try: # E
		if "".join([board[i - k][j] for k in range(4)]) in possibility:
			return [(i - 1, j), (i - 2, j)]
	except:
		pass
	try: # A
		if "".join([board[i - k][j - k] for k in range(4)]) in possibility:
			return [(i - 1, j - 1), (i - 2, j - 2)]
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(4)]) in possibility:
			return [(i + 1, j + 1), (i + 1, j + 2)]
	except:
		pass
	try: # C
		if "".join([board[i - k][j + k] for k in range(4)]) in possibility:
			return [(i - 1, j + 1), (i - 1, j + 2)]
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(4)]) in possibility:
			return [(i + 1, j - 1), (i + 2, j - 2)]
	except:
		pass
	return None

def pair_can_be_capture(board: list[list[str]], i, j) -> list[tuple[int]] | None:
	possibility = ("WBBW", "BWWB")
	try: # F
		if "".join([board[i][j + k] for k in range(4)]) in possibility:
			return [(i, j + 1), (i, j + 2)]
	except:
		pass
	try: # I
		if "".join([board[i][j - k] for k in range(4)]) in possibility:
			return [(i, j - 1), (i, j - 2)]
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(4)]) in possibility:
			return [(i + 1, j), (i + 2, j)]
	except:
		pass
	try: # E
		if "".join([board[i - k][j] for k in range(4)]) in possibility:
			return [(i - 1, j), (i - 2, j)]
	except:
		pass
	try: # A
		if "".join([board[i - k][j - k] for k in range(4)]) in possibility:
			return [(i - 1, j - 1), (i - 2, j - 2)]
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(4)]) in possibility:
			return [(i + 1, j + 1), (i + 1, j + 2)]
	except:
		pass
	try: # C
		if "".join([board[i - k][j + k] for k in range(4)]) in possibility:
			return [(i - 1, j + 1), (i - 1, j + 2)]
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(4)]) in possibility:
			return [(i + 1, j - 1), (i + 2, j - 2)]
	except:
		pass
	return None

def remove_pair_capture(board: list[list[str]]) -> dict | None:
	for i in range(len(board)):
		for j in range(len(board[i])):
			value = pair_can_be_capture(board, i, j)
			if value:
				return {'stone_attack': board[i][j], 'coordinate_to_remove': value}
	return None

def winner_found(board: list[list[str]]) -> tuple[bool, str | None]:
	for i in range(len(board)):
		for j in range(len(board[i])):
			if win_from_pos(board, i, j) == True:
				return (True, board[i][j])
	return (False, None)

def terminate_state(board: list[list[str]], black_capture: int = 0, white_capture: int = 0) -> bool:
	print(black_capture)
	print(white_capture)
	if black_capture >= 5 or white_capture >= 5:
		print("HERE")
		return True
	if winner_found(board)[0] == True:
		return True
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == ' ':
				return False
	return True # Tie

if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D5", "W")
	gomoku.place_stone(f"E5", "W")
	print(remove_pair_capture(gomoku.board))
	gomoku.place_stone(f"F5", "B")
	print(remove_pair_capture(gomoku.board))
	# HORIZONTAL
	# t = 3
	# for i in range(9):
	# 	if i % 2 == 0:
	# 		gomoku.place_stone(f"C{t}")
	# 		t += 1
	# 	else:
	# 		gomoku.place_stone(f"I{i + 1}")

	# VERTICAL
	# gomoku.place_stone(f"C5", "B")
	# gomoku.place_stone(f"D5", "B")
	# gomoku.place_stone(f"E5", "B")
	# gomoku.place_stone(f"F5", "B")
	# gomoku.place_stone(f"G5", "B")
	# for i in range(6, 10):
	# 	gomoku.place_stone(f"I{i}", "W")

	# DIAGONAL
	# gomoku.place_stone(f"C5", "B")
	# gomoku.place_stone(f"D6", "B")
	# gomoku.place_stone(f"E7", "B")
	# gomoku.place_stone(f"F8", "B")
	# gomoku.place_stone(f"G9", "B")
	# for i in range(6, 10):
	# 	gomoku.place_stone(f"I{i}", "W")

	# TIE
	# for i in range(len(gomoku.board)):
	# 	for j in range(len(gomoku.board[i])):
	# 		gomoku.board[i][j] = 'B'



	# print(gomoku)
	# print(terminate_state(gomoku.board))
	pass
