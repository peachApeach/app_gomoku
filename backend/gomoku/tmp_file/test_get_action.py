import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku

if __name__ == "__main__":
	gomoku = Gomoku()
	try:
		gomoku.read_a_game(17, 0, live_visualisation=False, live_speed=0.5)
	except Exception as e:
		print(e)
		pass
	print(gomoku)
