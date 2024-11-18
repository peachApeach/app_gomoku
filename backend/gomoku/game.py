#!/bin/python3

from srcs.Gomoku import Gomoku
from srcs.rules.GomokuSettings import GomokuSettings
from srcs.utils.Colors import *
from my_cli.CLI_OneSelection import CLI_OneSelection
from my_cli.CLI_MultipleSelection import CLI_MultipleSelection

def main():
	cli_mode = CLI_OneSelection("Mode ?")
	cli_mode.add_option("IA", "1 Player")
	cli_mode.add_option("noIA", "2 Players")
	cli_mode.run()

	if cli_mode.get_selection() == "IA":
		cli_start = CLI_OneSelection("Who starts ?")
		cli_start.add_option("player", "Player")
		cli_start.add_option("ia", "IA")
		cli_start.run()

		IA = True
		main_player = "B" if cli_start.get_selection() == "player" else "W"
	else:
		IA = False
		main_player = "B"

	cli_opening = CLI_OneSelection("Which opening you want ?")
	cli_opening.add_option("standard", "Standard")
	cli_opening.add_option("pro", "Pro")
	cli_opening.add_option("swap", "Swap")
	cli_opening.run()

	opening = cli_opening.get_selection()

	cli_game_opts = CLI_MultipleSelection("Select options you want to play with.")
	cli_game_opts.add_option("allowed_capture", "Allow capturing opponent's stones.", True)
	cli_game_opts.add_option("allowed_win_by_capture", "Allow winning by capturing 5 opponent's stones.", True)
	cli_game_opts.add_option("allowed_double_three", "Allow moves that create a double three.", False)
	cli_game_opts.run()

	game_opts = cli_game_opts.get_options()

	cli_save_game = CLI_OneSelection("Do you want to save the game ?")
	cli_save_game.add_option("yes", "Yes")
	cli_save_game.add_option("no", "No")
	cli_save_game.run()

	save_game = True if cli_save_game.get_selection() == "yes" else False

	try:
		gomoku = Gomoku(
			IA=IA,
			main_player=main_player,
			save_game=save_game,
			settings=GomokuSettings(
				allowed_capture=game_opts['allowed_capture'],
				allowed_win_by_capture=game_opts['allowed_win_by_capture'],
				allowed_double_three=game_opts['allowed_double_three']
			)
		)
		gomoku.play(opening=opening)

	except Exception as e:
		error_msg = f"{URED}{BHRED}Error{RESET}\n"
		error_msg += f"{BHRED}Name: {RED}{type(e).__name__}\n"
		error_msg += f"{BHRED}Message: {RED}{e}\n"
		print(error_msg)
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()
