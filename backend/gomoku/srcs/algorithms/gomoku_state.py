from rules.GomokuSettings import GomokuSettings

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
		for k in range(number_to_win):
			if stone_catchable(board, i, j + k) != None:
				raise Exception
		return True
	except:
		pass

	# VERTICAL
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j]:
				raise Exception
		for k in range(number_to_win):
			if stone_catchable(board, i + k, j) != None:
				raise Exception
		return True
	except:
		pass
	# DIAGONALE #1
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j + k]:
				raise Exception
		for k in range(number_to_win):
			if stone_catchable(board, i + k, j + k) != None:
				raise Exception
		return True
	except:
		pass
	# DIAGONALE #2
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j - k]:
				raise Exception
		for k in range(number_to_win):
			if stone_catchable(board, i + k, j - k) != None:
				raise Exception
		return True
	except:
		pass
	return False

def five_alignments_found(board: list[list[str]], i, j) -> bool:
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
	# DIAGONALE #1
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j + k]:
				raise Exception
		return True
	except:
		pass
	# DIAGONALE #2
	try:
		for k in range(number_to_win):
			if stone != board[i + k][j - k]:
				raise Exception
		return True
	except:
		pass
	return False

def critical_situation(board: list[list[str]], observed_stone: str = None) -> tuple[bool, str | None]:
	for i in range(len(board)):
		for j in range(len(board[i])):
			if observed_stone != None and board[i][j] != observed_stone:
				continue
			if five_alignments_found(board, i, j) == True:
				return (True, board[i][j])
	return (False, None)


def stone_catchable(board: list[list[str]], i, j):
	if board[i][j] == "B":
		possibility = ("WBB ", " BBW")
	else:
		possibility = ("BWW ", " WWB")

	try: # F
		if "".join([board[i][j + k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # I
		if "".join([board[i][j - k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # E
		if "".join([board[i - k][j] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # A
		if "".join([board[i - k][j - k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # C
		if "".join([board[i - k][j + k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(-1, 3)]) in possibility:
			return True
	except:
		pass
	return None

def winner_found(board: list[list[str]]) -> tuple[bool, str | None]:
	for i in range(len(board)):
		for j in range(len(board[i])):
			if win_from_pos(board, i, j) == True:
				return (True, board[i][j])

	return (False, None)

# from LittleGomoku import LittleGomoku
def terminate_state(gomoku) -> bool:
	# print(gomoku_settings)
	if gomoku.settings.allowed_win_by_capture == True and (gomoku.black_capture >= 5 or gomoku.white_capture >= 5):
		return True

	if gomoku.five_aligned_black >= 1 or gomoku.five_aligned_white >= 1:
		if gomoku.settings.allowed_capture == True:
			if winner_found(gomoku.board)[0] == True:
				return True
		else:
			if critical_situation(gomoku.board)[0] == True:
				return True

	for i in range(len(gomoku.board)):
		for j in range(len(gomoku.board[i])):
			if gomoku.board[i][j] == ' ':
				return False
	return True # Tie

if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone("B2", "B")
	gomoku.place_stone("C3", "B")
	gomoku.place_stone("D3", "W")
	gomoku.place_stone("D4", "B")
	gomoku.place_stone("D5", "B")
	gomoku.place_stone("E5", "B")
	gomoku.place_stone("F6", "B")
	print(terminate_state(gomoku))
	print(critical_situation(gomoku.board))
	print(stone_catchable(gomoku.board, 3, 3))
	print(gomoku)
	# gomoku.place_stone("B2", "B")
