import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_rules import *
from Gomoku import Gomoku

def test_terminate_state():
	# HORIZONTAL
	gomoku = Gomoku()
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
		gomoku.place_stone(f"I{i}", "W")

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
		gomoku.place_stone(f"I{i}", "W")

	assert winner_found(gomoku.board)[0] == True
	assert terminate_state(gomoku.board) == True

	gomoku = Gomoku(board_size=(4, 4))
	for i in range(len(gomoku.board)):
		for j in range(len(gomoku.board[i])):
			gomoku.board[i][j] = 'B'
	assert winner_found(gomoku.board)[0] == False
	assert terminate_state(gomoku.board) == True


def test_count_free_three():
	os.system('clear')
	gomoku = Gomoku()
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


if __name__ == "__main__":
	test_count_free_three()
