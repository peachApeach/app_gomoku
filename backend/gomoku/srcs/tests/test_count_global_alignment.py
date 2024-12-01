import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
import pytest

@pytest.fixture
def gomoku():
	return Gomoku()

def test_alignment_vertical(gomoku):
	gomoku.place_stone("G10", "B")
	gomoku.place_stone("H10", "B")
	gomoku.place_stone("I10", "W")
	gomoku.place_stone("F10", "B")
	assert gomoku.three_aligned_black == 1
	gomoku.place_stone("E10", "B")
	assert gomoku.three_aligned_black == 0
	assert gomoku.four_aligned_black == 1
	print(gomoku)

def test_alignment_horizontal(gomoku):
	gomoku.place_stone("I9", "B")
	gomoku.place_stone("K11", "W")
	gomoku.place_stone("I10", "B")

	assert gomoku.free_three_black == 0
	gomoku.place_stone("I11", "B")
	assert gomoku.free_three_black == 1
	print(gomoku)


if __name__ == "__main__":
	test_alignment_horizontal(Gomoku())
