# The black pieces starts first
# To win : Get 5 pieces in a row : Vertical, Horizontal, Diagonal
# In some rules, this line must be exactly five stones long; six or more stones in a row does not count as a win and is called an overline. : In the context of this
# projet, we will consider 5 or more to be a win.
# If the board is completely filled and no one has made a line of 5 stones, then the game ends in a draw.
# Gomoku will be played on a 19x19 Goban, without limit to the number of stones.
# Swap2 opening
# https://en.wikipedia.org/wiki/Gomoku#Variants

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.Colors import *
import string
import os
from utils.gomoku_utils import *
from utils.little_gomoku_utils import convert_to_little_gomoku
from algorithms.gomoku_state import *
from rules.gomoku_rules import *
from utils.my_utils import print_error
from rules.GomokuSettings import GomokuSettings
from algorithms.handle_alignment import count_all_alignment
from utils.MeasureTime import MeasureTime
import logging
import re
import time
import random

class GomokuError(Exception):
	pass

class PlacementError(Exception):
	pass

class Gomoku:
	def __init__(
			self,
			board_size: tuple[int, int] = (19, 19),
			IA: bool = True,
			IA_suggestion: bool = False,
			ia_against_ia: bool = False,
			who_start: str = 'B',
			save_game: bool = False,
			settings: GomokuSettings = GomokuSettings(),
			IA_MAX_DEPTH: int = 2,
			main_player: str = 'B',
	):
		self.IA = IA
		self.IA_suggestion = IA_suggestion
		self.__board_width = board_size[0]
		self.__board_height = board_size[1]
		self.save_game = save_game
		self.ia_against_ia = ia_against_ia
		self.IA_MAX_DEPTH = IA_MAX_DEPTH
		self.main_player = main_player
		self.who_start = who_start
		self.player_turn = who_start
		self.maximizing_player = who_start
		self.minimizing_player = 'W' if who_start == 'B' else 'B'
		self.settings = settings
		self.board = [[" " for _ in range(self.__board_width)] for __ in range(self.__board_height)]

		self.game_history_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "game_history")
		if self.save_game == True:
			i = 0
			while True:
				game_history_file = os.path.join(self.game_history_path, f"game_{i}.log")
				if os.path.isfile(game_history_file):
					i += 1
				else:
					break
			logging.basicConfig(level=logging.INFO,
					filename=game_history_file,
					filemode="w",
					encoding="utf_8",
					format=f'GameNumber : {i} - %(message)s'
					)

			logging.info(f"Game Info -> Start: {who_start}")
			logging.info(f"Game Info -> Allowed Capture: {settings.allowed_capture}")
			logging.info(f"Game Info -> Allowed Win By Capture: {settings.allowed_win_by_capture}")
			logging.info(f"Game Info -> Allowed Double Three: {settings.allowed_double_three}")

		# Default score
		self.black_capture = 0
		self.white_capture = 0

		self.three_aligned_black = 0
		self.three_aligned_white = 0

		self.free_three_black = 0
		self.free_three_white = 0

		self.four_aligned_black = 0
		self.four_aligned_white = 0

		self.free_four_black = 0
		self.free_four_white = 0

	def __str__(self) -> str:
		content = "  "
		for i in range(1, self.__board_width + 1):
			if i < 10:
				content += f"{i}  "
			else:
				content += f"{i} "
		content += "\n\n"
		for line, letters in zip(self.board, string.ascii_uppercase):
			content += f"{letters} "
			for char in line:
				if char == 'B':
					content += f"{BLACKB}  {RESET} "
				elif char == 'W':
					content += f"{WHITEHB}  {RESET} "
				elif char == ' ':
					content += f"{BLACKHB}  {RESET} "
				else:
					content += f"{REDHB}??{RESET} "

			content += "\n\n"
		return content

	def get_board_width(self):
		return self.__board_width
	def get_board_height(self):
		return self.__board_height

	def switch_player_turn(self):
		self.player_turn = 'B' if self.player_turn == 'W' else 'W'

	def get_player_turn(self) -> str:
		return self.player_turn

	def place_stone(self, coordinate: str, stone: str = None, force: bool = False):
		j, i = convert_coordinate_to_xy(coordinate)
		if i is None or j is None:
			raise PlacementError("Your coordinates are in invalid format. Except: 'LETTERS:NUMBER'")

		if j < 0 or j >= self.__board_width or i < 0 or i >= self.__board_height:
			raise PlacementError("Your coordinates is out of the board.")

		if force == True:
			self.board[i][j] = self.get_player_turn() if stone == None else stone
			return

		if self.board[i][j] == ' ' or stone == ' ':
			to_place = self.get_player_turn() if stone == None else stone
			if self.settings.allowed_capture == True:
				pairs_captured = pair_can_be_capture(self.board, i, j, to_place)
			else:
				pairs_captured = []

			before_placement_alignment = count_all_alignment(self.board, i, j)
			self.board[i][j] = to_place
			if pairs_captured != []:
				if self.board[i][j] == 'B':
					self.black_capture += len(pairs_captured)
				else:
					self.white_capture += len(pairs_captured)
				for pair in pairs_captured:
					cd1 = pair[0]
					cd2 = pair[1]
					self.board[cd1[0]][cd1[1]] = ' '
					self.board[cd2[0]][cd2[1]] = ' '
				after_placement_alignment = count_all_alignment(self.board, i, j)
			else:
				if self.settings.allowed_capture:
					situation = critical_situation(self.board)
					if situation[0] == True:
						if situation[1] != to_place:
							self.board[i][j] = ' '
							raise PlacementError("You are in a critical situation. Please fix this !")

				after_placement_alignment = count_all_alignment(self.board, i, j)

				if self.settings.allowed_double_three == False:
					if to_place == "B":
						if after_placement_alignment['free_three_black'] - before_placement_alignment['free_three_black'] >= 2:
							self.board[i][j] = ' '
							raise PlacementError("Your coordinates will create a double-three, this is forbidden.")
					else:
						if after_placement_alignment['free_three_white'] - before_placement_alignment['free_three_white'] >= 2:
							self.board[i][j] = ' '
							raise PlacementError("Your coordinates will create a double-three, this is forbidden.")
		else:
			raise PlacementError("This slot is already use. Please choose an other.")

		self.three_aligned_black += after_placement_alignment['three_aligned_black'] - before_placement_alignment['three_aligned_black']
		self.three_aligned_white += after_placement_alignment['three_aligned_white'] - before_placement_alignment['three_aligned_white']

		self.free_three_black += after_placement_alignment['free_three_black'] - before_placement_alignment['free_three_black']
		self.free_three_white += after_placement_alignment['free_three_white'] - before_placement_alignment['free_three_white']

		self.four_aligned_black += after_placement_alignment['four_aligned_black'] - before_placement_alignment['four_aligned_black']
		self.four_aligned_white += after_placement_alignment['four_aligned_white'] - before_placement_alignment['four_aligned_white']

		self.free_four_black += after_placement_alignment['free_four_black'] - before_placement_alignment['free_four_black']
		self.free_four_white += after_placement_alignment['free_four_white'] - before_placement_alignment['free_four_white']

	def display_board(self, message: str | None = None, is_err: bool = False, last_duration: str | None = None, all_informations: bool = False, allow_suggestion: bool = False):
		from algorithms.gomoku_algorithm import minimax
		os.system("clear")
		if (message != None):
			print()
			if is_err:
				print(f"{BHRED} ==== ERROR : {message} ===={RESET}")
			else:
				print(f"{BHWHITE} ==== STATE : {message} ===={RESET}")
		print(self)
		print(f"{BLACKB}{BHWHITE}BLACK HAS CAPTURED {self.black_capture} WHITE PAIRS.{RESET}")
		print(f"{WHITEHB}{BHBLACK}WHITE HAS CAPTURED {self.white_capture} BLACK PAIRS.{RESET}")

		if all_informations:
			print(f"{BLACKB}{BHWHITE}")
			# print()
			print(f"Aligned three black : {self.three_aligned_black}")
			print(f"Free Three black : {self.free_three_black}")
			print(f"Aligned four black : {self.four_aligned_black}")
			print(f"Free four black : {self.free_four_black}{RESET}")


			print(f"{WHITEHB}{BHBLACK}")
			print(f"Aligned three white : {self.three_aligned_white}")
			print(f"Free Three white : {self.free_three_white}")
			print(f"Aligned four white : {self.four_aligned_white}")
			print(f"Free four white : {self.free_four_white}{RESET}")

		if last_duration:
			print(f"{BHWHITE}IA Reflexion Duration :{MAGB} {last_duration} {RESET}")
		if allow_suggestion and self.IA_suggestion:
			score, move = minimax(gomoku=convert_to_little_gomoku(self), MAX_DEPTH=self.IA_MAX_DEPTH)
			print(f"{BHWHITE}IA Suggestion :{GREENB} {convert_xy_to_coordinate(move[1], move[0])} | {score} {RESET}")
		print()

	def opening_pro(self):
		second_move = False
		third_move = False
		is_err = False
		message = None

		# MIDDLE J10 (9, 9)
		self.place_stone("J10")
		self.switch_player_turn()

		south_east = ("K11", "L12", "M13", "N14", "O15", "P16", "Q17", "R18", "S19")
		south_east_coordinate = (
			(10, 10),
			(11, 11),
			(12, 12),
			(13, 13),
			(14, 14),
			(15, 15),
			(16, 16),
			(17, 17),
			(18, 18),
			(19, 19),
		)
		message = "PRO OPENING : Place the next stone in south east."
		while not second_move:
			self.display_board(message=message, is_err=is_err)
			if self.ia_against_ia == True:
				placement = random.choice(south_east[0:2])
			else:
				color = f'{BLACKB}{BHWHITE} (Black) {RESET}' if self.get_player_turn() == 'B' else f'{WHITEB}{BHBLACK} (White) {RESET}'
				if self.IA == False:
					if self.main_player == self.get_player_turn():
						prompt = f"{color} - Player 1 Turn -> "
					else:
						prompt = f"{color} - Player 2 Turn -> "
					placement = input(prompt)
				else:
					if self.main_player == self.get_player_turn():
						prompt = f"{color} - Your Turn -> "
						placement = input(prompt)
					else:
						placement = random.choice(south_east[0:2])

			if convert_coordinate_to_xy(placement) not in south_east_coordinate:
				message = "PRO OPENING : You need to place the stone in south east."
				is_err = True
				continue
			try:
				self.place_stone(placement)
				self.switch_player_turn()
			except Exception as e:
				message = e
				is_err = True
				continue

			second_move = True
			is_err = False

		# THREE AWAY
		message = "PRO OPENING : Place the stone at least three intersections away from the first stone."
		while not third_move:
			self.display_board(message=message, is_err=is_err)
			if self.ia_against_ia == True:
				rdm_action = random.choice(opening_pro_get_actions(self.board))
				placement = convert_xy_to_coordinate(rdm_action[1], rdm_action[0])
			else:
				color = f'{BLACKB}{BHWHITE} (Black) {RESET}' if self.get_player_turn() == 'B' else f'{WHITEB}{BHBLACK} (White) {RESET}'
				if self.IA == False:
					if self.main_player == self.get_player_turn():
						prompt = f"{color} - Player 1 Turn -> "
					else:
						prompt = f"{color} - Player 2 Turn -> "
					placement = input(prompt)
				else:
					if self.main_player == self.get_player_turn():
						prompt = f"{color} - Your Turn -> "
						placement = input(prompt)
					else:
						rdm_action = random.choice(opening_pro_get_actions(self.board))
						placement = convert_xy_to_coordinate(rdm_action[1], rdm_action[0])

			convert_coordinate = convert_coordinate_to_xy(placement)

			if calcul_distance_between_two_points(convert_coordinate, (9, 9)) <= 2:
				message = "PRO OPENING : The stone must be placed at least three intersections away from the first stone."
				is_err = True
				continue
			try:
				self.place_stone(placement)
				self.switch_player_turn()
				third_move = True
			except Exception as e:
				message = e
				is_err = True
				continue

	def opening_swap(self):
		from algorithms.gomoku_algorithm import minimax
		if self.ia_against_ia == True:
			return
		is_err = False
		message = None

		stone_placed = 0
		message = "SWAP OPENING : First player places three stones."
		while stone_placed < 3:
			if is_err == False:
				message = f"SWAP OPENING : First player places {3 - stone_placed} stone{'s' if 3 - stone_placed > 1 else ''}."
				if stone_placed == 0 or stone_placed == 2:
					message += " Black stone in your hands."
				else:
					message += " White stone in your hands."
			self.display_board(message=message, is_err=is_err)

			if self.IA == False:
				if self.main_player == self.who_start:
					prompt = "Opening - Player 1 Turn -> "
				else:
					prompt = "Opening - Player 2 Turn -> "
				placement = input(prompt)
			else:
				if self.main_player == self.who_start:
					prompt = f"Opening - Your Turn -> "
					placement = input(prompt)
				else:
					rdm_action = random.choice(opening_swap_get_actions(self.board))
					placement = convert_xy_to_coordinate(rdm_action[1], rdm_action[0])
			try:
				self.place_stone(placement)
				self.switch_player_turn()
				stone_placed += 1
				is_err = False
			except Exception as e:
				message = e
				is_err = True
				continue

		message = "SWAP OPENING : Swap ?"
		while True:
			self.display_board(message=message, is_err=is_err)
			if self.IA == False:
				if self.main_player == self.who_start:
					prompt = "Player 2, which color you want to play ? (b/w) -> "
				else:
					prompt = "Player 1, which color you want to play ? (b/w) -> "
				user_choice = input(prompt).upper()
			else:
				if self.main_player != self.who_start:
					user_choice = input("Which color you want to play ? (b/w) -> ").upper()
				else:
					score, move = minimax(convert_to_little_gomoku(self), MAX_DEPTH=2)
					if score <= 0:
						user_choice = self.minimizing_player
					else:
						user_choice = self.maximizing_player

			if user_choice != "B" and user_choice != "W":
				message = "Please enter a valid value -> (b/w)"
				is_err = True
				continue
			else:
				if self.main_player != self.who_start:
					self.main_player = user_choice
				else:
					self.main_player = "B" if user_choice == "W" else "W"
				break

	def handle_opening(self, opening: str):
		opening = opening.lower()
		if opening == "pro":
			self.opening_pro()
		elif opening == "swap":
			self.opening_swap()

	def read_a_game(self, n: int, stop_read: int, live_visualisation: bool = False, live_speed: float = 1.5):
		filename = os.path.join(self.game_history_path, f"game_{n}.log")
		try:
			with open(filename, "r") as f:
				all_steps = f.read().splitlines()
				if len(all_steps) == 0:
					return
		except Exception as e:
			print_error(e)
			return

		self.player_turn = all_steps[0][-1]
		self.maximizing_player = self.player_turn
		self.minimizing_player = 'W' if self.player_turn == 'B' else 'B'

		allowed_capture = True if all_steps[1].split()[-1] == "True" else False
		allowed_win_by_capture = True if all_steps[2].split()[-1] == "True" else False
		allowed_double_three = True if all_steps[3].split()[-1] == "True" else False
		self.settings = GomokuSettings(allowed_capture, allowed_win_by_capture, allowed_double_three)
		try:
			all_steps = all_steps[4:]
			if stop_read == 0:
				pass
			elif stop_read < 0:
				all_steps = all_steps[0:stop_read]
			else:
				all_steps = all_steps[stop_read:]
		except Exception as e:
			print_error(e)
		for step in all_steps:
			cut_step = step.split(":")
			player = cut_step[-2][0]
			if player != self.player_turn:
				self.switch_player_turn()

			self.place_stone(cut_step[-1])
			if live_visualisation:
				self.display_board()
				print(f"{player} has placed in {cut_step[-1]}")
				time.sleep(live_speed)
			self.switch_player_turn()


	def handle_player(self) -> list:
		from algorithms.gomoku_algorithm import minimax

		color = f'{BLACKB}{BHWHITE} (Black) {RESET}' if self.get_player_turn() == 'B' else f'{WHITEB}{BHBLACK} (White) {RESET}'
		mt = MeasureTime(start=True)

		# It's Human Turn
		if self.ia_against_ia == False and (self.get_player_turn() == self.main_player or self.IA == False):
			while True:
				if self.ia_against_ia == True:
					score, move = minimax(gomoku=convert_to_little_gomoku(self), MAX_DEPTH=self.IA_MAX_DEPTH)
					user_placement = convert_xy_to_coordinate(move[1], move[0])
				else:
					if self.IA == False:
						if self.main_player == self.get_player_turn():
							prompt = f"{color} - Player 1 Turn -> "
						else:
							prompt = f"{color} - Player 2 Turn -> "
					else:
						prompt = f"{color} - Your Turn -> "
					user_placement = input(prompt)
				try:
					self.place_stone(user_placement)
					log_str_time = mt.stop(get_str=True, duration_only=True)

					if self.save_game:
						logging.info(f"{log_str_time.ljust(12)} - Player    :{self.get_player_turn()} -> Move:{user_placement}")

					self.switch_player_turn()
					break
				except Exception as e:
					message = str(e)
					is_err = True
					self.display_board(message=message, is_err=is_err)
			last_duration = None
		# It's IA Turn
		else:
			score, move = minimax(gomoku=convert_to_little_gomoku(self), MAX_DEPTH=self.IA_MAX_DEPTH)
			ia_placement = convert_xy_to_coordinate(move[1], move[0])
			last_duration = mt.stop(get_str=True, duration_only=True)
			try:
				self.place_stone(ia_placement)
				if self.save_game:
					logging.info(f"{last_duration.ljust(12)} - Player(IA):{self.get_player_turn()} -> Move:{ia_placement}")
				self.switch_player_turn()
				last_duration += f" | Score: {score} | Move: {ia_placement}"
			except Exception as e:
				print_error(e)
				print(move)
				print(ia_placement)
				print(f"{BHRED}Sorry, the IA cannot continue the game, you win by forfeit...{RESET}")
				exit(1)


		return last_duration

	def play(self, opening: str = "standard"):
		is_err = False
		message = None
		last_duration = None
		self.handle_opening(opening)
		while terminate_state(self.board, self.black_capture, self.white_capture, self.settings) == False:
			is_err = False
			message = f"Is {'black' if self.get_player_turn() == 'B' else 'white'} player turn."
			self.display_board(message=message, last_duration=last_duration, is_err=is_err, allow_suggestion=True)
			last_duration = self.handle_player()

		if self.settings.allowed_capture:
			if self.black_capture >= 5 or self.white_capture >= 5:
				has_winner = True
				who_win = "B" if self.black_capture >= 5 else "W"
			else:
				has_winner, who_win = winner_found(self.board)
		else:
			has_winner, who_win = critical_situation(self.board)
		is_err = False
		if has_winner:
			message = f"{'White' if who_win == 'W' else 'Black'} has won the game !"
		else:
			message = "No one has won. It's a perfect tie !"
		self.display_board(message=message, is_err=is_err)


	def run(self):
		from algorithms.gomoku_algorithm import minimax

		# It's Human Turn
		if self.get_player_turn() == self.main_player or self.IA == False:
			return self.board
		# It's IA Turn
		else:
			score, move = minimax(gomoku=convert_to_little_gomoku(self), MAX_DEPTH=self.IA_MAX_DEPTH)
			ia_placement = convert_xy_to_coordinate(move[1], move[0])
			try:
				self.place_stone(ia_placement)
				self.switch_player_turn()
				return self.board
			except Exception:
				return None

	def apply_move(self, x: int, y: int) -> str | None:
		from algorithms.gomoku_algorithm import minimax
		user_placement = convert_xy_to_coordinate(x, y)
		self.place_stone(user_placement)
		self.switch_player_turn()
		if self.get_player_turn() != self.main_player and self.IA == True:
			score, move = minimax(gomoku=convert_to_little_gomoku(self), MAX_DEPTH=self.IA_MAX_DEPTH)
			ia_placement = convert_xy_to_coordinate(move[1], move[0])
			self.place_stone(ia_placement)
			self.switch_player_turn()


	def timeout(self):
		pass


if __name__ == "__main__":
	from algorithms.gomoku_algorithm import minimax
	SIMULATION = False
	if SIMULATION:
		# settings = GomokuSettings(allowed_capture=False, allowed_win_by_capture=False, allowed_double_three=True)
		go_simulate = Gomoku(ia_against_ia=False)
		go_simulate.read_a_game(31, -2, live_visualisation=False, live_speed=0.1)
		go_simulate.play()
	else:
		settings = GomokuSettings(allowed_capture=True, allowed_win_by_capture=True, allowed_double_three=False)
		AGAINST_HUMAN = True
		gomoku = Gomoku(
			IA=True,
			who_start="B", # Always Black
			main_player="B",
			save_game=False,
			settings=settings,
			ia_against_ia=not AGAINST_HUMAN,
			IA_suggestion=True,
			IA_MAX_DEPTH=2)
		gomoku.play(opening="pro")

