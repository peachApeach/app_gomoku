from srcs.Gomoku import Gomoku
from srcs.utils.Colors import *
from srcs.utils.little_gomoku_utils import convert_to_little_gomoku

if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R18", "W")
	gomoku.place_stone("C16", "B")

	lg = convert_to_little_gomoku(gomoku)

	for action in lg.get_actions():
		print(lg.simulate_action(action))

	lg.paint_actions(lg.get_actions(), live_visualisation=True)
	# print(gomoku)
