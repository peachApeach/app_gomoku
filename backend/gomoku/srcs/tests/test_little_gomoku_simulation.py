import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import *
from utils.little_gomoku_utils import convert_to_little_gomoku
from utils.gomoku_utils import convert_coordinate_to_xy
import pytest

@pytest.fixture
def gomoku():
	return Gomoku()

def test_double_three_fail_simulation_opponent_pov(gomoku): # Subject example
	gomoku.place_stone("E7", "W")
	gomoku.place_stone("F8", "W")
	gomoku.place_stone("H11", "W")
	gomoku.place_stone("H12", "W")
	lg = convert_to_little_gomoku(gomoku=gomoku)
	assert lg.player_turn == "B"
	with pytest.raises(PlacementError):
		j, i = convert_coordinate_to_xy("H10")
		lg.do_simulation((i, j), opponent_pov=True)
	assert lg.player_turn == "B"
	print(gomoku)
