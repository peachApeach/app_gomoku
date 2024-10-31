
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

def pair_can_be_capture(board: list[list[str]], i, j) -> list[tuple[int]] | None:
	stone = board[i][j]
	if stone == ' ':
		return None
	# HORIZONTAL
	try:
		if	stone == board[i][j + 3] and\
			board[i][j + 1] == board[i][j + 2] and\
			board[i][j + 2] != board[i][j + 3] and\
			board[i][j + 1] != ' ':
			return [(i, j + 1), (i, j + 2)]
		raise Exception
	except:
		pass

	# VERTICAL
	try:
		if	stone == board[i + 3][j] and\
			board[i + 1][j] == board[i + 2][j] and\
			board[i + 2][j] != board[i + 3][j] and\
			board[i + 1][j] != ' ':
			return [(i + 1, j), (i + 2, j)]
		raise Exception
	except:
		pass
	# DIAGONALE
	try:
		if	stone == board[i + 3][j + 3] and\
			board[i + 1][j + 1] == board[i + 2][j + 2] and\
			board[i + 2][j + 2] != board[i + 3][j + 3] and\
			board[i + 1][j + 1] != ' ':
			return [(i + 1, j + 1), (i + 2, j + 2)]
		raise Exception
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
