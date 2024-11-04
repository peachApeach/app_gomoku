
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

def stone_catchable(board: list[list[str]], i, j):
	stone = board[i][j]
	opposite_stone = 'B' if stone == 'W' else 'W'
	
	print(board[i][j])
	pass

def winner_found(board: list[list[str]]) -> tuple[bool, str | None]:
	for i in range(len(board)):
		for j in range(len(board[i])):
			if win_from_pos(board, i, j) == True:
				return (True, board[i][j])

	return (False, None)

def terminate_state(board: list[list[str]], black_capture: int = 0, white_capture: int = 0) -> bool:
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
	gomoku.place_stone("B2", "B")
	gomoku.place_stone("C3", "B")
	gomoku.place_stone("D3", "W")
	gomoku.place_stone("D4", "B")
	gomoku.place_stone("D5", "B")
	gomoku.place_stone("E5", "B")
	gomoku.place_stone("F6", "B")
	print(terminate_state(gomoku.board))
	print(stone_catchable(gomoku.board, 3, 3))
	print(gomoku)
	# gomoku.place_stone("B2", "B")
