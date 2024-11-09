from gomoku_state import terminate_state, winner_found, critical_situation
from LittleGomoku import LittleGomoku

def game_state(gomoku: LittleGomoku) -> int:
	"""
	**********************
	* HEURISTIC FUNCTION *
	**********************
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


	Value of thing :
	5 stones aligned: 100
	5 stones aligned: 80
	Free Four: 70
	4 stones aligned not obstructed: 60
	Free Three: 50
	3 stones aligned: 40
	# == PAIRS ==
	5 pairs catched: 100
	4 pairs catched: 40
	3 pairs catched: 30
	2 pairs catched: 20
	1 pairs catched: 10
	# == ===== ==
	0
	Make substraction of Maximizing Player Score and Minimizing Player Score
	We doesn't need to know you player turn is

	if max_player == BLACK:
		black_score - white_score
	else
		white_score - black_score
	"""
	value = 0
	# print(gomoku_settings)
	if gomoku.settings.allowed_win_by_capture == True and (gomoku.black_capture >= 5 or gomoku.white_capture >= 5):
		value = 5
	if gomoku.settings.allowed_capture == True:
		if winner_found(gomoku.board)[0] == True:
			value = 5
	else:
		if critical_situation(gomoku.board)[0] == True:
			value = 4


	for i in range(len(gomoku.board)):
		for j in range(len(gomoku.board[i])):
			if gomoku.board[i][j] == ' ':
				return False
	return True # Tie
	if gomoku.player_turn == gomoku.maximizing_player:
		return random.randint(1, 5)
	else:
		return random.randint(-5, -1)
