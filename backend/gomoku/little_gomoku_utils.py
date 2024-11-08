def get_actions_range(board: list[list[str]], radius: int = 1):
	"""
	Pour un tableau, ca nous renvoie l'area de jeu a checker. Pour eviter de parcourir les 19x19 cases a chaque fois, ca peut etre reduit a 6x6 par exemple. On peut aussi gerer largeur du cercle de range.
	"""
	min_i = None
	max_i = None
	min_j = float("+inf")
	max_j = float("-inf")
	for i in range(len(board)):
		for j in range(len(board[i])):
			if board[i][j] != ' ':
				if min_i is None:
					min_i = i
				max_i = i + 1
				if j < min_j:
					min_j = j
				if j > max_j:
					max_j = j + 1


	min_i = min_i - radius if min_i - radius >= 0 else 0
	min_j = min_j - radius if min_j - radius >= 0 else 0

	max_i = max_i + radius if max_i + radius <= len(board[min_i]) else len(board[min_i])
	max_j = max_j + radius if max_j + radius <= len(board[min_i]) else len(board[min_i])


	print(f"Range i : ({min_i}, {max_i})")
	print(f"Range j : ({min_j}, {max_j})")
	return (range(min_i, max_i), range(min_j, max_j))





if __name__ == "__main__":
	from Gomoku import Gomoku
	from MeasureTime import MeasureTime
	from LittleGomoku import LittleGomoku
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	# gomoku.place_stone("R18", "W")
	# gomoku.place_stone("B2", "B")
	gomoku.switch_player_turn()

	littleGomoku = LittleGomoku(
		board=gomoku.board,
		player_turn=gomoku.player_turn,
		gomoku_settings=gomoku.settings,
		max_player=gomoku.maximizing_player,
		min_player=gomoku.minimizing_player,
		black_capture=gomoku.black_capture,
		white_capture=gomoku.white_capture,
		free_three_black=gomoku.free_three_black,
		free_three_white=gomoku.free_three_white,
		board_width=gomoku.get_board_width(),
		board_height=gomoku.get_board_height())


	measureTime = MeasureTime(start=True)
	range_i, range_j = get_actions_range(littleGomoku.board)
	measureTime.stop()
	print(littleGomoku)
	for i in range_i:
		for j in range_j:
			littleGomoku.board[i][j] = '_'
	print(littleGomoku)
