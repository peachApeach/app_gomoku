import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import *
from LittleGomoku import LittleGomoku
import pytest


@pytest.fixture
def gomoku():
	return Gomoku()

def test_get_actions_only_one_move_possible(gomoku):
	gomoku.place_stone("B2", "W")
	gomoku.place_stone("C3", "W")
	gomoku.place_stone("D5", "W")
	gomoku.place_stone("E5", "W")
	gomoku.place_stone("F6", "W")

	gomoku.place_stone("D3", "B")
	gomoku.place_stone("H3", "B")
	gomoku.place_stone("I4", "B")
	gomoku.place_stone("I5", "B")
	gomoku.place_stone("H10", "B")


	gomoku.place_stone("D4", "W")

	littleGomoku = LittleGomoku(
		board=gomoku.board,
		player_turn=gomoku.player_turn,
		gomoku_settings=gomoku.settings,
		max_player=gomoku.maximizing_player,
		min_player=gomoku.minimizing_player,
		black_capture=gomoku.black_capture,
		white_capture=gomoku.white_capture,
		free_three_black=gomoku.free_three_black,
		free_three_white=gomoku.free_three_white)

	assert littleGomoku.get_actions() == [(5, 3)]
	print(littleGomoku.get_actions())

	# with pytest.raises(PlacementError):
	print(gomoku)
	# gomoku.place_stone("D6", "B")
	# gomoku.place_stone("L11", "B")
	print(gomoku)
	pass

if __name__ == "__main__":
	test_get_actions_only_one_move_possible(Gomoku())
	pass
