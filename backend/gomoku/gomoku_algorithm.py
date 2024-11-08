from gomoku_state import terminate_state
from GomokuSettings import GomokuSettings
from LittleGomoku import LittleGomoku
import time
import random

class GomokuIAError(Exception):
	pass

def game_state(gomoku: LittleGomoku) -> tuple[int, str]:
	"""
	**********************
	* HEURISTIC FUNCTION *
	**********************

	Ca renvoie la valeur du tableau.

	End Game Conditions (TERMINATE = TRUE):
	[6] - 5 stones aligned unbreakable
	[5] - 5 pairs catched
	[0] - No space left on board

	Good issue (TERMINATE = FALSE):
	[4] - 5 stones aligned
	[3] - Free Four
	[2] - Free Three
	[1] - More stone catch
	# - (?) No Free Three for opponent (?)
	# - No Free Four for opponent
	"""
	pass

def simulate_action(gomoku: LittleGomoku) -> LittleGomoku:
	"""
	Ca cree un nouveau littleGomoku, avec le nouveau player turn, un nouveau board tout neuf et on retransmet les settings.
	"""
	pass

def minimax(
	gomoku: LittleGomoku,
	alpha: float = float("-inf"),
	beta: float = float("+inf"),
	DEPTH: int = 0,
	MAX_DEPTH: int = 1
):
	# MAX_DEPTH : 1 : 352ms
	# MAX_DEPTH : 2 : 17539ms
	# print("=====================")
	# print(f"===== DEPTH : {DEPTH} =====")
	# print("=====================")
	if DEPTH == MAX_DEPTH:
		# return random.randint(-5, 5), None
		return 0, None
	# if terminate_state(board) or DEPTH == MAX_DEPTH:
	# 	return game_state(gomoku), None

	if gomoku.player_turn == gomoku.maximizing_player:
		value = float('-inf')
		best_action = None
		for action in gomoku.get_actions():
			try:
				new_gomoku = gomoku.simulate_action(action)
			except:
				continue
			state, r_action = minimax(new_gomoku, alpha, beta, DEPTH + 1, MAX_DEPTH=MAX_DEPTH)

			if state > value:
				value = state
				best_action = action

			alpha = max(alpha, state)
			if beta <= alpha or state == 1:
				break
		return value, best_action

	elif gomoku.player_turn == gomoku.minimizing_player:
		value = float('+inf')
		best_action = None
		for action in gomoku.get_actions():
			try:
				new_gomoku = gomoku.simulate_action(action)
			except:
				continue
			state, r_action = minimax(new_gomoku, alpha, beta, DEPTH + 1, MAX_DEPTH=MAX_DEPTH)

			if state < value:
				value = state
				best_action = action
			beta = min(beta, state)
			if beta <= alpha or state == -1:
				break
		return value, best_action
	else:
		raise GomokuIAError(f"Invalid player turn : {gomoku.player_turn}")


if __name__ == "__main__":
	from Gomoku import Gomoku
	from MeasureTime import MeasureTime
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R18", "W")
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

	print(gomoku)
	# gomoku.board[3][1] = "W"
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)


	measureTime = MeasureTime(start=True)
	# print(littleGomoku.get_actions())
	print(minimax(littleGomoku, MAX_DEPTH=2))
	measureTime.stop()

	from gomoku_rules import is_creating_db_free_three, is_free_three
	# print(is_creating_db_free_three(littleGomoku.board, 3, 1, "W"))
	# littleGomoku.board[7][5] = "W"
	# print(is_free_three(littleGomoku.board, 7, 5, "W"))
	print(littleGomoku)


