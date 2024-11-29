import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import *
import pytest


@pytest.fixture
def gomoku():
	return Gomoku()


def test_double_three_creation_1(gomoku): # Subject example
	gomoku.place_stone("E7", "B")
	gomoku.place_stone("F8", "B")
	gomoku.place_stone("H11", "B")
	gomoku.place_stone("H12", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("H10", "B")
	print(gomoku)

def test_double_three_creation_2(gomoku):
	gomoku.place_stone("E9", "B")
	gomoku.place_stone("F8", "B")
	gomoku.place_stone("F10", "B")
	gomoku.place_stone("G9", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("F9", "B")
	print(gomoku)

def test_double_three_creation_3(gomoku):
	gomoku.place_stone("E9", "B")
	gomoku.place_stone("E10", "B")
	gomoku.place_stone("F11", "B")
	gomoku.place_stone("G11", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("E11", "B")
	print(gomoku)

def test_double_three_creation_4(gomoku):
	gomoku.place_stone("E9", "B")
	gomoku.place_stone("E10", "B")
	gomoku.place_stone("F8", "B")
	gomoku.place_stone("G8", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("E8", "B")
	print(gomoku)


def test_double_three_creation_5(gomoku): # Subject example reverse
	gomoku.place_stone("E16", "B")
	gomoku.place_stone("F15", "B")
	gomoku.place_stone("H11", "B")
	gomoku.place_stone("H12", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("H13", "B")
	print(gomoku)

def test_double_three_creation_T(gomoku): # Subject example reverse
	gomoku.place_stone("E8", "B")
	gomoku.place_stone("E10", "B")
	gomoku.place_stone("F9", "B")
	gomoku.place_stone("G9", "B")
	with pytest.raises(PlacementError):
		gomoku.place_stone("E9", "B")
	print(gomoku)

if __name__ == "__main__":
	test_double_three_creation_T(Gomoku())
