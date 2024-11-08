import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_rules import *
from Gomoku import *
import pytest

@pytest.fixture
def gomoku():
	return Gomoku()


def test_terminate_state(gomoku):
	# HORIZONTAL
	t = 3
	for i in range(9):
		if i % 2 == 0:
			gomoku.place_stone(f"C{t}")
			t += 1
		else:
			gomoku.place_stone(f"I{i + 1}")

	assert winner_found(gomoku.board)[0] == True

	# VERTICAL
	gomoku = Gomoku()
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D5", "B")
	gomoku.place_stone(f"E5", "B")
	gomoku.place_stone(f"F5", "B")
	gomoku.place_stone(f"G5", "B")
	for i in range(6, 10):
		gomoku.place_stone(f"I{i}", "W", force=True)

	assert winner_found(gomoku.board)[0] == True
	assert terminate_state(gomoku.board) == True

	# DIAGONAL
	gomoku = Gomoku()
	gomoku.place_stone(f"C5", "B")
	gomoku.place_stone(f"D6", "B")
	gomoku.place_stone(f"E7", "B")
	gomoku.place_stone(f"F8", "B")
	gomoku.place_stone(f"G9", "B")
	for i in range(6, 10):
		gomoku.place_stone(f"I{i}", "W", force=True)

	assert winner_found(gomoku.board)[0] == True
	assert terminate_state(gomoku.board) == True

	gomoku = Gomoku(board_size=(4, 4))
	for i in range(len(gomoku.board)):
		for j in range(len(gomoku.board[i])):
			gomoku.board[i][j] = 'B'
	assert winner_found(gomoku.board)[0] == False
	assert terminate_state(gomoku.board) == True


def test_count_free_three(gomoku):
	# gomoku = Gomoku()
	gomoku.place_stone("C5", "B")
	gomoku.place_stone("D6", "B")
	gomoku.place_stone("F8", "B")
	assert count_free_three(gomoku.board, 'B') == 1
	gomoku.place_stone("F9", "B")
	print(gomoku.free_three_black)
	gomoku.place_stone("F10", "B")
	print(gomoku.free_three_black)
	assert count_free_three(gomoku.board, 'B') == 2
	gomoku.place_stone("H6", "B")
	gomoku.place_stone("I5", "B")
	assert count_free_three(gomoku.board, 'B') == 3

	print(gomoku)


# def test_create_double_free_three(gomoku):
# 	gomoku.place_stone("C5", "B")
# 	gomoku.place_stone("D6", "B")
# 	gomoku.place_stone("F9", "B")
# 	gomoku.place_stone("F10", "B")
# 	with pytest.raises(PlacementError):
# 		gomoku.place_stone("F8", "B")
# 	print(gomoku)

def test_create_double_free_three_1(gomoku):
	gomoku.place_stone("C5", "B")
	gomoku.place_stone("D6", "B")

	gomoku.place_stone("C8", "B")
	gomoku.place_stone("D8", "B")

	gomoku.place_stone("C11", "B")
	gomoku.place_stone("D10", "B")

	gomoku.place_stone("F10", "B")
	gomoku.place_stone("F11", "B")

	gomoku.place_stone("H10", "B")
	gomoku.place_stone("I11", "B")

	gomoku.place_stone("H8", "B")
	gomoku.place_stone("I8", "B")

	gomoku.place_stone("H6", "B")
	gomoku.place_stone("I5", "B")

	gomoku.place_stone("F5", "B")
	gomoku.place_stone("F6", "B")

	assert is_creating_db_free_three(gomoku.board, 5, 7, "B") == True
	# gomoku.place_stone("F8","B", force=True)

	# print(gomoku)

def test_breaking_line_warning(gomoku):
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
	with pytest.raises(PlacementError):
		gomoku.place_stone("L11", "B")
	print(gomoku)

def test_breaking_line(gomoku):
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
	gomoku.place_stone("D6", "B")
	# with pytest.raises(PlacementError):
	# 	gomoku.place_stone("L11", "B")
	print(gomoku)

if __name__ == "__main__":
	os.system('clear')
	# test_breaking_line(Gomoku())
	test_create_double_free_three_1(Gomoku())

# if __name__ == "__main__":
# 	go = Gomoku()
# 	go.place_stone("B5")
# 	go.place_stone("B6")
# 	go.place_stone("C5")
# 	go.place_stone("D6")

# 	# go.place_stone("B4")

# 	print(go)
