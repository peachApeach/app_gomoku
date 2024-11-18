#!/bin/python3

from srcs.Gomoku import Gomoku
from srcs.utils.Colors import *
import random
from my_cli.CLI_OneSelection import CLI_OneSelection
from my_cli.CLI_MultipleSelection import CLI_MultipleSelection

def main():

	cli_mode = CLI_OneSelection("Mode ?")
	cli_mode.add_option("IA", "1 Player")
	cli_mode.add_option("noIA", "2 Players")

	cli_mode.run()
	mode = cli_mode.get_selection()
	if mode == "IA":
		cli_start = CLI_OneSelection("Who starts ?")
		cli_start.add_option("player", "Player")
		cli_start.add_option("ia", "IA")
		cli_start.run()

	cli_opening = CLI_OneSelection("Which opening you want ?")
	cli_opening.add_option("standard", "Standard")
	cli_opening.add_option("pro", "Pro")
	cli_opening.add_option("swap", "Swap")

	cli_opening.run()

	cli_game_opts = CLI_MultipleSelection("Select options you want to play with.")
	cli_game_opts.add_option("allowed_capture", "Allow capturing opponent's stones.", True)
	cli_game_opts.add_option("allowed_win_by_capture", "Allow winning by capturing 5 opponent's stones.", True)
	cli_game_opts.add_option("allowed_double_three", "Allow moves that create a double three.", False)

	cli_game_opts.run()

	cli_savegame = CLI_OneSelection("Do you want to save the game ?")
	cli_savegame.add_option("yes", "Yes")
	cli_savegame.add_option("no", "No")

	cli_savegame.run()




	exit(1)
	try:
		pass

	except Exception as e:
		error_msg = f"{URED}{BHRED}Error{RESET}\n"
		error_msg += f"{BHRED}Name: {RED}{type(e).__name__}\n"
		error_msg += f"{BHRED}Message: {RED}{e}\n"
		print(error_msg)

if __name__ == "__main__":
	main()
