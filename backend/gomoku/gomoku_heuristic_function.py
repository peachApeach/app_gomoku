from gomoku_state import critical_situation
from gomoku_rules import count_all_three
from LittleGomoku import LittleGomoku

def game_state(gomoku: LittleGomoku, advantage_next_player: bool = False) -> int:
	"""
	************************
	* HEURISTIC FUNCTION   *
	************************
	* EXCEPT TIME < 5MS ✅ *
	************************
	C'est uniquement lorsqu'on atteint une terminate state or DEPTH == MAX_DEPTH que cette fonction est appelé. Donc ce n'est pas nécessaire d'appeler les fonctions pour compter constamment à par celle pour les stones capturées.
	Ca renvoie la valeur du tableau.

	End Game Conditions (TERMINATE = TRUE):
	[5] Victory = Max value - 5 stones aligned unbreakable ✅
	[5] Victory = Max value - 5 pairs catched ✅
	[0] Tie = No good- No space left on board

	Good issue (TERMINATE = FALSE):
	[4] - 5 stones aligned
	[3] - Free Four
	[2] - Free Three
	[1] - More stone catch
	# - (?) No Free Three for opponent (?)
	# - No Free Four for opponent


	All possiblities :
	1 Free Three et l'adversaire 0 Free Three
	1 Free Four et l'adversaire 0 Free Four
	+ Free Three que l'adverse
	+ Free Four que l'adverse
	Si rien de tout ça, + de paires capturées que l'adverse
	L'égalité est peut-être une bonne solution ?

	# == ===== ==
	0
	Make substraction of Maximizing Player Score and Minimizing Player Score
	We doesn't need to know you player turn is

	if max_player == BLACK:
		black_score - white_score
	else
		white_score - black_score
	"""


	# Value of thing : (S_ = Score)
	# 5 stones aligned: 100
	# 5 stones aligned: 80
	S_FIVE_ALIGNED = 15000
	# Free Four: 70
	S_FREE_FOUR = 3000
	# 4 stones aligned not obstructed: 60
	S_FOUR_ALIGNED = 1500
	# Free Three: 50
	S_FREE_THREE = 1000
	# 3 stones aligned: 40
	S_THREE_ALIGNED = 100


	# # == PAIRS ==
	pairs = {
		'0': 0,
		'1': 50,
		'2': 200,
		'3': 400,
		'4': 2500,
		'5': 15000
	}
	# # 5 pairs catched: 100
	# S_5_PAIR_CAPTURED = 50
	# # 4 pairs catched: 40
	# S_4_PAIR_CAPTURED = 50
	# # 3 pairs catched: 30
	# S_3_PAIR_CAPTURED = 50
	# # 2 pairs catched: 20
	# S_2_PAIR_CAPTURED = 50
	# # 1 pairs catched: 10
	# S_1_PAIR_CAPTURED = 50


	score_white = 0
	score_black = 0

	########################################
	# FIVE ALIGNED
	########################################
	five_exists, who_critical = critical_situation(gomoku.board)
	if five_exists == True:
		if who_critical == 'B':
			score_black += S_FIVE_ALIGNED
		else:
			score_white += S_FIVE_ALIGNED

	########################################
	# FREE FOUR
	########################################
	score_black += gomoku.free_four_black * S_FREE_FOUR
	score_white += gomoku.free_four_white * S_FREE_FOUR

	########################################
	# FOUR ALIGNED
	########################################
	score_black += gomoku.four_aligned_black * S_FOUR_ALIGNED
	score_white += gomoku.four_aligned_white * S_FOUR_ALIGNED

	########################################
	# FREE THREE
	########################################
	score_black += gomoku.free_three_black * S_FREE_THREE
	score_white += gomoku.free_three_white * S_FREE_THREE

	########################################
	# THREE ALIGNED
	########################################
	score_black += gomoku.three_aligned_black * S_THREE_ALIGNED
	score_white += gomoku.three_aligned_white * S_THREE_ALIGNED

	########################################
	# PAIRS CATCHED
	########################################

	if gomoku.settings.allowed_win_by_capture == True:
		if gomoku.black_capture > 5:
			score_black += pairs['5']
		else:
			score_black += pairs[f'{gomoku.black_capture}']
		if gomoku.white_capture > 5:
			score_white += pairs['5']
		else:
			score_white += pairs[f'{gomoku.white_capture}']


	# print(f"Black player scores => {score_black}")
	# print(f"White player scores => {score_white}")

	if score_black == score_white:
		"""
		Si DEPTH == MAX_DEPTH, il se peut que le score de prochain joueur soit plus dangereux, donc on ajuste les scores pour envisager le pire.
		"""
		if gomoku.player_turn == "B":
			score_black *= 1.5
		else:
			score_white *= 1.5

	if gomoku.maximizing_player == "B":
		return score_black - score_white
	else:
		return score_white - score_black

if __name__ == "2__main__2":
	from Gomoku import Gomoku
	from gomoku_algorithm import minimax
	from MeasureTime import MeasureTime

	gomoku = Gomoku()
	gomoku.place_stone("H6", "B")
	gomoku.place_stone("J9", "W")
	gomoku.place_stone("H7", "B")
	gomoku.place_stone("J3", "W")
	gomoku.place_stone("H8", "B")
	gomoku.place_stone("J8", "W")
	gomoku.place_stone("H9", "B")
	gomoku.place_stone("J10", "W")

	gomoku.place_stone("H2", "W")
	gomoku.place_stone("H4", "W")
	gomoku.place_stone("H5", "W")

	gomoku.place_stone("H11", "W")
	gomoku.place_stone("H12", "W")
	gomoku.place_stone("H13", "W")

	for i in range(7, 11):
		gomoku.place_stone(f"C{i}", "W")

	for i in range(9, 13):
		gomoku.place_stone(f"E{i}", "W")
	gomoku.place_stone(f"E13", "B")

	gomoku.place_stone("H16", "B")
	gomoku.place_stone("H10", "B")

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

	print(littleGomoku)
	mt = MeasureTime(start=True)
	# for i in range(200):
	# 	game_state(littleGomoku)
	# iteration = 361
	iteration = 1000
	print(f"TIMER START FOR {iteration} ITERATIONS")
	for i in range(iteration):
		game_state(littleGomoku)
	# game_state(littleGomoku)
	# game_state(littleGomoku)
	# game_state(littleGomoku)
	mt.stop()
	from gomoku_rules import count_all_three
	print(count_all_three(littleGomoku.board, "W"))



if __name__ == "__main__":
	from Gomoku import Gomoku
	from gomoku_algorithm import minimax
	from MeasureTime import MeasureTime
	# gomoku = Gomoku()
	# gomoku.place_stone("G6", "B")
	# gomoku.place_stone("H7", "W")
	# gomoku.place_stone("J3", "B")
	# # gomoku.place_stone("H8", "W")
	# gomoku.place_stone("J8", "B")
	# gomoku.place_stone("H9", "W")
	# gomoku.place_stone("J10", "B")
	# gomoku.place_stone("R17", "W")
	# # gomoku.place_stone("R18", "W")
	# gomoku.switch_player_turn()

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
	for _ in range(400):
		actions = littleGomoku.get_actions()
	# littleGomoku.paint_actions(actions)
	# print(actions)
	print(minimax(littleGomoku, MAX_DEPTH=1))
	measureTime.stop()
	# littleGomoku.paint_actions(actions)
	# print(is_creating_db_free_three(littleGomoku.board, 3, 1, "W"))
	# littleGomoku.board[7][5] = "W"
	# print(is_free_three(littleGomoku.board, 7, 5, "W"))
	print(littleGomoku)
