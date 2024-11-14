import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku


if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.place_stone("G8", "B")
	gomoku.place_stone("G9", "W")
	gomoku.place_stone("G10", "W")
	gomoku.place_stone("H11", "W")
	gomoku.place_stone("I11", "W")
	gomoku.place_stone("J11", "B")

	# gomoku.place_stone("G11", "B")
	print(gomoku)
	print(gomoku.black_capture)
	print(gomoku.white_capture)
	gomoku.place_stone("G11", "B")
	print(gomoku)
	print(gomoku.black_capture)
	print(gomoku.white_capture)

