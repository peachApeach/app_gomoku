
def stone_is_a_menace(board: list[list[str]], i: int, j: int, radius: int = 1):
	"""
	Pour ne pas prendre en compte les pierres isoles dans le champ des actions
	"""
	stone = board[i][j]
	count_same = 0
	min_i = i - radius if i - radius >= 0 else 0
	min_j = j - radius if j - radius >= 0 else 0

	max_i = i + 1 + radius if i + 1 + radius <= len(board) else len(board)
	max_j = j + 1 + radius if j + 1 + radius <= len(board[min_i]) else len(board[min_i])

	for i in range(min_i, max_i):
		for j in range(min_j, max_j):
			if board[i][j] == stone:
				count_same += 1
			# littleGomoku.board[i][j] = '_'
	return count_same > 1

def is_useful_placement(board: list[list[str]], i: int, j: int, stone: str, radius: int = 2):
	"""
	Pour ne pas prendre en compte les pierres isoles dans le champ des actions
	"""
	count_same = 0
	count_different = 0
	min_i = i - radius if i - radius >= 0 else 0
	min_j = j - radius if j - radius >= 0 else 0

	max_i = i + 1 + radius if i + 1 + radius <= len(board) else len(board)
	max_j = j + 1 + radius if j + 1 + radius <= len(board[min_i]) else len(board[min_i])

	for i in range(min_i, max_i):
		for j in range(min_j, max_j):
			if board[i][j] != ' ':
				if board[i][j] == stone:
					count_same += 1
				else:
					count_different += 1

	return count_same, count_different
	# return count_same > 0 or count_different > 1

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
			if board[i][j] != ' ' and stone_is_a_menace(board, i, j, radius=2) == True:
				if min_i is None:
					min_i = i
				max_i = i
				if j < min_j:
					min_j = j
				if j > max_j:
					max_j = j

	if min_i is None or max_i is None or min_j is float or max_j is float:
		return (None, None)

	min_i = min_i - radius - 1 if min_i - radius - 1 >= 0 else 0
	min_j = min_j - radius - 1 if min_j - radius - 1>= 0 else 0

	max_i = max_i + radius + 1 if max_i + radius + 1 <= len(board) else len(board)
	max_j = max_j + radius + 1 if max_j + radius + 1 <= len(board[min_i]) else len(board[min_i])
	return (range(min_i, max_i), range(min_j, max_j))


def convert_to_little_gomoku(gomoku):
	from LittleGomoku import LittleGomoku
	return LittleGomoku(
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
		five_aligned_black=gomoku.five_aligned_black,
		five_aligned_white=gomoku.five_aligned_white,
		free_four_black=gomoku.free_four_black,
		free_four_white=gomoku.free_four_white,
		board_width=gomoku.get_board_width(),
		board_height=gomoku.get_board_height())




if __name__ == "__main__":
	import sys
	import os
	sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	from Gomoku import Gomoku
	from utils.MeasureTime import MeasureTime
	from LittleGomoku import LittleGomoku
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R18", "W")
	# gomoku.place_stone("R17", "W")
	# gomoku.place_stone("B2", "B")
	# gomoku.switch_player_turn()

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
	range_i, range_j = get_actions_range(littleGomoku.board, radius=1)
	measureTime.stop()
	print(littleGomoku)
	for i in range_i:
		for j in range_j:
			littleGomoku.board[i][j] = '_'
	# stone_is_a_menace(littleGomoku.board, 2, 2, radius=2)
	# stone_is_a_menace(littleGomoku.board, 9, 2, radius=2)
	print(littleGomoku)
