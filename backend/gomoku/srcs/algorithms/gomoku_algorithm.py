from algorithms.gomoku_state import terminate_state
from LittleGomoku import LittleGomoku
from algorithms.gomoku_heuristic_function import game_state

class GomokuIAError(Exception):
	pass

def get_max_depth(gomoku: LittleGomoku, DEPTH: int, MAX_DEPTH: int):
	# state = game_state(gomoku, True)
	# if state == 0:
	# 	return DEPTH + 1
	if gomoku.five_aligned_black >= 1 or gomoku.five_aligned_white >= 1:
		return min(DEPTH + 1, MAX_DEPTH)
	if gomoku.free_four_black >= 1:
		if gomoku.player_turn == "B":
			return min(DEPTH + 2, MAX_DEPTH)
		else:
			return min(DEPTH + 3, MAX_DEPTH)
	if gomoku.free_four_white >= 1:
		if gomoku.player_turn == "W":
			return min(DEPTH + 2, MAX_DEPTH)
		else:
			return min(DEPTH + 3, MAX_DEPTH)

	if gomoku.free_three_black >= 2:
		return min(DEPTH + 3, MAX_DEPTH)
		# if gomoku.player_turn == "B":
		# 	return DEPTH + 1
		# else:
		# 	return DEPTH + 2
	if gomoku.free_three_white >= 2:
		return min(DEPTH + 3, MAX_DEPTH)
		# if gomoku.player_turn == "W":
		# 	return DEPTH + 1
		# else:
		# 	return DEPTH + 2


	# if gomoku.free_four_black >= 1 or gomoku.free_four_white >= 1:
	# 	return DEPTH + 1
	# if gomoku.four_aligned_black >= 1 or gomoku.four_aligned_white >= 1:
	# 	return DEPTH + 1
	else:
		return MAX_DEPTH

# MARCHE TRÈS BIEN AVEC MAX_DEPTH=2
def minimax(
	gomoku: LittleGomoku,
	alpha: float = float("-inf"),
	beta: float = float("+inf"),
	actions: list[tuple[int]] = None,
	DEPTH: int = 0,
	MAX_DEPTH: int = 1
):
	# MAX_DEPTH : 1 : 352ms
	# MAX_DEPTH : 2 : 17539ms
	# print("=====================")
	# print(f"===== DEPTH : {DEPTH} =====")
	# print("=====================")

	if terminate_state(
		gomoku
		):
		return game_state(gomoku, False), None

	if DEPTH == MAX_DEPTH:
		return game_state(gomoku, False), None

	if gomoku.player_turn == gomoku.maximizing_player:
		value = float('-inf')
		best_action = None
		MAX_DEPTH = get_max_depth(gomoku, DEPTH, MAX_DEPTH)
		if actions is None:
			actions = gomoku.get_actions()
		for action in actions:
			try:
				new_gomoku = gomoku.simulate_action(action)
			except:
				# print("Failed to simulate")
				continue
			state, r_action = minimax(gomoku=new_gomoku, alpha=alpha, beta=beta, DEPTH=DEPTH + 1, MAX_DEPTH=MAX_DEPTH)

			if state > value:
				value = state
				best_action = action

			alpha = max(alpha, state)
			if beta <= alpha:# or state >= 5000:# or state == 6:
				break
		return value, best_action

	elif gomoku.player_turn == gomoku.minimizing_player:
		value = float('+inf')
		best_action = None
		MAX_DEPTH = get_max_depth(gomoku, DEPTH, MAX_DEPTH)
		if actions is None:
			actions = gomoku.get_actions()
		for action in actions:
			try:
				new_gomoku = gomoku.simulate_action(action)
			except:
				continue
			state, r_action = minimax(gomoku=new_gomoku, alpha=alpha, beta=beta, DEPTH=DEPTH + 1, MAX_DEPTH=MAX_DEPTH)

			if state < value:
				value = state
				best_action = action
			beta = min(beta, state)
			# print(f"{beta} | {state}")
			if beta <= alpha:# or state <= -5000: # or state == -6:
				break
		return value, best_action
	else:
		raise GomokuIAError(f"Invalid player turn : {gomoku.player_turn}")


def super_minimax(
	gomoku: LittleGomoku,
	alpha: float = float("-inf"),
	beta: float = float("+inf"),
	actions: list[tuple[int]] = None,
	DEPTH: int = 0,
	MAX_DEPTH: int = 4
):
	# MAX_DEPTH : 1 : 352ms
	# MAX_DEPTH : 2 : 17539ms
	# print("=====================")
	# print(f"===== DEPTH : {DEPTH} =====")
	# print("=====================")
	gomoku.minimax_node += 1
	if terminate_state(
		gomoku
		):
		return game_state(gomoku, False), None

	if DEPTH >= MAX_DEPTH:
		return game_state(gomoku, False), None


	if gomoku.player_turn == gomoku.maximizing_player:
		value = float('-inf')
		best_action = None
		if actions is None:
			actions = gomoku.super_get_actions()
		for action in actions:
			try:
				gomoku_state = gomoku.do_simulation(action)
				MAX_DEPTH = get_max_depth(gomoku, DEPTH, MAX_DEPTH)
				state, r_action = super_minimax(gomoku=gomoku, alpha=alpha, beta=beta, DEPTH=DEPTH + 1, MAX_DEPTH=MAX_DEPTH)
				gomoku.undo_simulation(gomoku_state)
			except:
				continue

			if state > value:
				value = state
				best_action = action

			alpha = max(alpha, state)
			if beta <= alpha:
				break
		return value, best_action

	elif gomoku.player_turn == gomoku.minimizing_player:
		value = float('+inf')
		best_action = None
		if actions is None:
			actions = gomoku.super_get_actions()
		for action in actions:
			try:
				gomoku_state = gomoku.do_simulation(action)
				MAX_DEPTH = get_max_depth(gomoku, DEPTH, MAX_DEPTH)
				state, r_action = super_minimax(gomoku=gomoku, alpha=alpha, beta=beta, DEPTH=DEPTH + 1, MAX_DEPTH=MAX_DEPTH)
				gomoku.undo_simulation(gomoku_state)
			except:
				continue

			if state < value:
				value = state
				best_action = action
			beta = min(beta, state)
			if beta <= alpha:
				break
		return value, best_action
	else:
		raise GomokuIAError(f"Invalid player turn : {gomoku.player_turn}")

def negamax(
	gomoku: LittleGomoku,
	alpha: float = float("-inf"),
	beta: float = float("+inf"),
	actions: list[tuple[int]] = None,
	DEPTH: int = 0,
	MAX_DEPTH: int = 1
):
	if terminate_state(gomoku) or DEPTH == MAX_DEPTH:
		mult = 1 if gomoku.player_turn == gomoku.maximizing_player else -1
		return mult * game_state(gomoku, False), None

	if actions is None:
			actions = gomoku.get_actions()

	value = float("-inf")
	best_action = None
	for action in actions:
		try:
			gomoku_state = gomoku.do_simulation(action)
			state = -(negamax(gomoku=gomoku, alpha=-beta, beta=-alpha, DEPTH=DEPTH + 1, MAX_DEPTH=MAX_DEPTH)[0])
			gomoku.undo_simulation(gomoku_state)
		except:
			continue
		print(f"ST : {state}")
		if state > value:
			value = state
			best_action = action

		alpha = max(alpha, state)
		if beta <= alpha:# or state >= 5000:# or state == 6:
			break
	return value, best_action



if __name__ == "__main__":
	from Gomoku import Gomoku
	from utils.MeasureTime import MeasureTime
	# PLACEMENT 1
	# gomoku = Gomoku()
	# gomoku.place_stone("G6", "B")
	# gomoku.place_stone("H7", "W")
	# gomoku.place_stone("J3", "B")
	# gomoku.place_stone("H8", "W")
	# gomoku.place_stone("J8", "B")
	# gomoku.place_stone("H9", "W")
	# gomoku.place_stone("J10", "B")
	# # gomoku.place_stone("R18", "W")
	# gomoku.switch_player_turn()
	# ###########

	# PLACEMENT 2
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
	# ###########

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
		board_width=gomoku.get_board_width(),
		board_height=gomoku.get_board_height())

	print(gomoku)
	# gomoku.board[3][1] = "W"
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)

	iteration = 1
	print("Measure Get Actions")
	measureTime = MeasureTime(start=True)
	for _ in range(iteration):
		littleGomoku.get_actions()
	measureTime.stop()

	# exit(1)
	print("Measure Game State")
	measureTime = MeasureTime(start=True)
	for _ in range(iteration):
		game_state(gomoku)
	measureTime.stop()

	print("Measure Minimax")
	measureTime = MeasureTime(start=True)
	score_state, optimal_move = minimax(gomoku=littleGomoku, MAX_DEPTH=4)
	measureTime.stop()

	# print(littleGomoku.get_actions())


	print(f"Score {score_state} | Optimal Move {optimal_move}")
	littleGomoku.board[optimal_move[0]][optimal_move[1]] = "??"

	# print(is_creating_db_free_three(littleGomoku.board, 3, 1, "W"))
	# littleGomoku.board[7][5] = "W"
	# print(is_free_three(littleGomoku.board, 7, 5, "W"))
	print(littleGomoku)


