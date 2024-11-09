import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from LittleGomoku import LittleGomoku
from Gomoku import Gomoku
import pytest

@pytest.fixture
def gomoku():
	return Gomoku()

def convert_to_little_gomoku(gomoku: Gomoku):
	return LittleGomoku(
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

from gomoku_heuristic_function import game_state




def test_free_three_advantage_min_player(gomoku: Gomoku):
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.switch_player_turn()
	# gomoku
	# gomoku.place_stone("R17", "W")

	littleGomoku = convert_to_little_gomoku(gomoku)

	print(littleGomoku)
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)

	assert game_state(littleGomoku) == -3

def test_free_three_advantage_max_player(gomoku: Gomoku):
	gomoku.place_stone("J9", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H19", "W")
	gomoku.place_stone("J10", "B")
	# gomoku.switch_player_turn()
	# gomoku
	# gomoku.place_stone("R17", "W")

	littleGomoku = convert_to_little_gomoku(gomoku)

	print(littleGomoku)
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)

	assert game_state(littleGomoku) == 3

if __name__ == "__main__":
	test_free_three_advantage_max_player(Gomoku())
