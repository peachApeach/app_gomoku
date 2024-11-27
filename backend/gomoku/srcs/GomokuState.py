class GomokuState:
	def __init__(self, gomoku, action: tuple[int]) -> None:
		self.saved_position = []
		self.__save_position(gomoku, action)

		self.player_turn = gomoku.player_turn

		self.black_capture = gomoku.black_capture
		self.white_capture = gomoku.white_capture

		self.three_aligned_black = gomoku.three_aligned_black
		self.three_aligned_white = gomoku.three_aligned_white

		self.four_aligned_black = gomoku.four_aligned_black
		self.four_aligned_white = gomoku.four_aligned_white

		self.free_three_black = gomoku.free_three_black
		self.free_three_white = gomoku.free_three_white

		self.free_four_black = gomoku.free_four_black
		self.free_four_white = gomoku.free_four_white

		self.five_aligned_black = gomoku.five_aligned_black
		self.five_aligned_white = gomoku.five_aligned_white

	def __save_position(self, gomoku, action: tuple[int]):
		# Action permettra d'enregistrer les actions que dans le rayon
		radius = 2
		i = action[0]
		j = action[1]

		min_i = i - radius if i - radius >= 0 else 0
		min_j = j - radius if j - radius >= 0 else 0

		max_i = i + 1 + radius if i + 1 + radius <= len(gomoku.board) else len(gomoku.board)
		max_j = j + 1 + radius if j + 1 + radius <= len(gomoku.board[min_i]) else len(gomoku.board[min_i])

		for i in range(min_i, max_i):
			for j in range(min_j, max_j):
				self.saved_position.append((i, j, gomoku.board[i][j]))
		# for i in range(len(gomoku.board)):
		# 	for j in range(len(gomoku.board[i])):
		# 		self.saved_position.append((i, j, gomoku.board[i][j]))

	def apply_on_board(self, gomoku):
		for position in self.saved_position:
			if gomoku.board[position[0]][position[1]] != position[2]:
				gomoku.board[position[0]][position[1]] = position[2]
			# gomoku.board[position[0]][position[1]] = "??"


if __name__ == "__main__":
	from LittleGomoku import LittleGomoku
	from Gomoku import Gomoku
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

	littleGomoku = LittleGomoku(
		board=gomoku.board,
		player_turn=gomoku.player_turn,
		gomoku_settings=gomoku.settings,
		max_player=gomoku.maximizing_player,
		min_player=gomoku.minimizing_player,
		black_capture=gomoku.black_capture,
		white_capture=gomoku.white_capture,
		three_aligned_black=gomoku.three_aligned_black,
		three_aligned_white=gomoku.three_aligned_white,
		free_three_black=gomoku.free_three_black,
		free_three_white=gomoku.free_three_white,
		four_aligned_black=gomoku.four_aligned_black,
		four_aligned_white=gomoku.four_aligned_white,
		free_four_black=gomoku.free_four_black,
		free_four_white=gomoku.free_four_white,
		five_aligned_black=gomoku.five_aligned_black,
		five_aligned_white=gomoku.five_aligned_white,
		board_width=gomoku.get_board_width(),
		board_height=gomoku.get_board_height())

	gomokuState = GomokuState(littleGomoku, (5, 10))
	# print(littleGomoku)
	# print(gomokuState.saved_position)

	gomoku = Gomoku()
	print(gomoku)
	gomokuState.apply_on_board(gomoku)
	print(gomoku)
	pass
