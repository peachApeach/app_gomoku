
def win_from_pos(board: list[list[str]], i, j) -> bool:
	stone = board[i][j]
	if stone == ' ':
		return False
	# HORIZONTAL
	try:
		for k in range(5):
			if stone != board[i][j + k]:
				raise Exception
		return True
	except:
		pass

	# VERTICAL
	try:
		for k in range(5):
			if stone != board[i + k][j]:
				raise Exception
		return True
	except:
		pass
	# DIAGONALE
	try:
		for k in range(5):
			if stone != board[i + k][j + k]:
				raise Exception
		return True
	except:
		pass
	return False

def winner_found(board: list[list[str]]) -> bool:
	for i in range(len(board)):
		for j in range(len(board[i])):
			if win_from_pos(board, i, j) == True:
				return True
	return False

def terminate_state(board: list[list[str]]) -> bool:
	if winner_found(board) == True:
		return True
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] == ' ':
				return False
	return True # Tie

if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()
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
