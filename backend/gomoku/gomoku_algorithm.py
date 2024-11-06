from gomoku_state import terminate_state
from GomokuSettings import GomokuSettings
from LittleGomoku import LittleGomoku

def state_board(gomoku: LittleGomoku) -> tuple[int, str]:
	"""
	**********************
	* HEURISTIC FUNCTION *
	**********************

	Ca renvoie la valeur du tableau.

	End Game Conditions :
	- 5 Blacks aligned
	- 5 Whites aligned
	- 5 Blacks pairs catched
	- 5 Whites pairs catched
	- No space left on board

	Good issue :
	- Free Three
	- Free Four
	- More stone catch
	"""
	pass

def get_actions(gomoku: LittleGomoku) -> list[str]:
	"""
	Ca renvoie toutes les actions qui ne raise aucune erreur.
	Donc on recupere toutes les cases vides, on les converti en ALPHA:NUM
	Puis on teste de les ajouter et retirer.
	Ne pas tester les cases en dehors d'un rayon de +2/3 du carré former par les pions pour eviter de tester les bords inutiles.
	"""
	pass

def simulate_action(gomoku: LittleGomoku) -> LittleGomoku:
	"""
	Ca cree un nouveau littleGomoku, avec le nouveau player turn, un nouveau board tout neuf et on retransmet les settings.
	"""
	pass

def minimax(
	board: list[list[str]],
	gomoku_settings: GomokuSettings,
	player_turn: str,
	alpha: float = float("-inf"),
	beta: float = float("+inf"),
	DEPTH: int = 0
):
	if terminate_state(board):
		pass

if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()
	gomoku.place_stone("A2", "B")
	gomoku.place_stone("A5", "W")
	gomoku.place_stone("B6", "B")
	gomoku.place_stone("E9", "W")
	gomoku.place_stone("G12", "B")
	gomoku.place_stone("G9", "W")
	print(gomoku)
