import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Gomoku import Gomoku
from utils.Colors import *
from utils.little_gomoku_utils import convert_to_little_gomoku

def get_actions_visualization(game_log_n: int, mode: str = "all", step: int = 1, start_iteration: int = 1, max_iteration: int = None):
	if mode == "all":
		i = start_iteration
		while max_iteration == None or i < max_iteration:
			gomoku = Gomoku()
			if gomoku.read_a_game(game_log_n, i) == -1:
				break
			lg = convert_to_little_gomoku(gomoku)
			lg.paint_actions(lg.ultimate_get_actions())
			print(lg)
			print(f"Step : {i} | player_turn : {lg.player_turn} | maximizing_player : {lg.maximizing_player} | minimizing_player {lg.minimizing_player}")
			print("=" * 30)
			i += 1
	elif mode == "step":
		gomoku = Gomoku()
		if gomoku.read_a_game(game_log_n, step) == -1:
			print("oos")
			return
		lg = convert_to_little_gomoku(gomoku)
		lg.paint_actions(lg.ultimate_get_actions())
		print(lg)
		print(f"Step : {step} | player_turn : {lg.player_turn} | maximizing_player : {lg.maximizing_player} | minimizing_player {lg.minimizing_player}")
	else:
		print("invalid move")

if __name__ == "__main__":
	get_actions_visualization(mode="all", game_log_n=44, start_iteration=10, max_iteration=20)
	# get_actions_visualization(mode="step", game_log_n=44, step=7)
