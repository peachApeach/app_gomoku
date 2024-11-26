from Gomoku import Gomoku
from algorithms.gomoku_algorithm import minimax, super_minimax
from utils.MeasureTime import MeasureTime
from LittleGomoku import LittleGomoku
import time

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

littleGomoku = LittleGomoku(
	board=gomoku.board,
	player_turn=gomoku.player_turn,
	gomoku_settings=gomoku.settings,
	max_player=gomoku.maximizing_player,
	min_player=gomoku.minimizing_player,
	black_capture=gomoku.black_capture,
	white_capture=gomoku.white_capture,
	three_aligned_black=gomoku.three_aligned_black,
	three_aligned_white=gomoku.three_aligned_white,
	free_three_black=gomoku.free_three_black,
	free_three_white=gomoku.free_three_white,
	four_aligned_black=gomoku.four_aligned_black,
	four_aligned_white=gomoku.four_aligned_white,
	free_four_black=gomoku.free_four_black,
	free_four_white=gomoku.free_four_white,
	board_width=gomoku.get_board_width(),
	board_height=gomoku.get_board_height())

print(gomoku)
# gomoku.board[3][1] = "W"
print(littleGomoku.player_turn)
print(littleGomoku.maximizing_player)
print(littleGomoku.minimizing_player)

# exit(1)

# measureTime = MeasureTime(start=True)
# minimax(littleGomoku, MAX_DEPTH=4)
# measureTime.stop()

# time.sleep(0.5)

measureTime = MeasureTime(start=True)
super_minimax(littleGomoku, MAX_DEPTH=10)
measureTime.stop()


