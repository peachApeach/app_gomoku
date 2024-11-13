# The black pieces starts first
# To win : Get 5 pieces in a row : Vertical, Horizontal, Diagonal
# In some rules, this line must be exactly five stones long; six or more stones in a row does not count as a win and is called an overline. : In the context of this
# projet, we will consider 5 or more to be a win.
# If the board is completely filled and no one has made a line of 5 stones, then the game ends in a draw.
# Gomoku will be played on a 19x19 Goban, without limit to the number of stones.
# Swap2 opening
# https://en.wikipedia.org/wiki/Gomoku#Variants

from Colors import *
import string
import os
from gomoku_utils import convert_coordinate_to_xy, convert_xy_to_coordinate
from little_gomoku_utils import convert_to_little_gomoku
from gomoku_state import *
from gomoku_rules import *
from my_utils import print_error
from GomokuSettings import GomokuSettings
from handle_alignment import count_all_alignment
from MeasureTime import MeasureTime
import logging
import re

class GomokuError(Exception):
	pass

class PlacementError(Exception):
	pass

class Gomoku:
	def __init__(self, board_size: tuple[int] = (19, 19), IA: bool = True, IA_suggestion: bool = False, who_start: str = 'B', save_game: bool = False, settings: GomokuSettings = GomokuSettings()):
		self.IA = IA
		self.IA_suggestion = IA_suggestion
		self.__board_width = board_size[0]
		self.__board_height = board_size[1]
		self.save_game = save_game
		if self.save_game == True:
			i = 0
			while True:
				if os.path.isfile(f"./game_history/game_{i}.log"):
					i += 1
				else:
					break
			logging.basicConfig(level=logging.INFO,
					filename=f"./game_history/game_{i}.log",
					filemode="w",
					encoding="utf_8",
					# format='entClass.py - %(asctime)s - %(levelname)s - %(message)s'
					format=f'GameNumber : {i} - %(message)s'
					)

			logging.info(f"Game Info -> Start: {who_start}")
			logging.info(f"Game Info -> Allowed Capture: {settings.allowed_capture}")
			logging.info(f"Game Info -> Allowed Win By Capture: {settings.allowed_win_by_capture}")
			logging.info(f"Game Info -> Allowed Double Three: {settings.allowed_double_three}")



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


		self.player_turn = who_start
		self.maximizing_player = who_start
		self.minimizing_player = 'W' if who_start == 'B' else 'B'

		self.settings = settings
		self.board = [[" " for _ in range(self.__board_width)] for __ in range(self.__board_height)]
		# print(self.board)"x", "o", " ", "x"

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

		if force:
			self.board[i][j] = self.get_player_turn() if stone == None else stone
			return

		if self.board[i][j] == ' ' or stone == ' ':
			to_place = self.get_player_turn() if stone == None else stone
			if self.settings.allowed_capture == True:
				value = pair_can_be_capture(self.board, i, j, to_place)
			else:
				value = None

			before_placement_alignment = count_all_alignment(self.board, i, j)
			self.board[i][j] = to_place
			if value:
				if self.board[i][j] == 'B':
					self.black_capture += 1
				else:
					self.white_capture += 1
				cd1 = value[0]
				cd2 = value[1]
				self.board[cd1[0]][cd1[1]] = ' '
				self.board[cd2[0]][cd2[1]] = ' '
				after_placement_alignment = count_all_alignment(self.board, i, j)
			else:
				# self.board[i][j] = to_place

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

		# if (stone == None):
		# 	print("BEFORE")
		# 	print(before_placement_alignment)
		# 	print("AFTER")
		# 	print(after_placement_alignment)

		self.three_aligned_black += after_placement_alignment['three_aligned_black'] - before_placement_alignment['three_aligned_black']
		self.three_aligned_white += after_placement_alignment['three_aligned_white'] - before_placement_alignment['three_aligned_white']

		self.free_three_black += after_placement_alignment['free_three_black'] - before_placement_alignment['free_three_black']
		self.free_three_white += after_placement_alignment['free_three_white'] - before_placement_alignment['free_three_white']

		self.four_aligned_black += after_placement_alignment['four_aligned_black'] - before_placement_alignment['four_aligned_black']
		self.four_aligned_white += after_placement_alignment['four_aligned_white'] - before_placement_alignment['four_aligned_white']

		self.free_four_black += after_placement_alignment['free_four_black'] - before_placement_alignment['free_four_black']
		self.free_four_white += after_placement_alignment['free_four_white'] - before_placement_alignment['free_four_white']

	def remove_pairs(self):
		value = remove_pair_capture(self.board)
		if value:
			if value['stone_attack'] == 'B':
				self.black_capture += 1
			else:
				self.white_capture += 1
			cd1 = value['coordinate_to_remove'][0]
			cd2 = value['coordinate_to_remove'][1]
			self.board[cd1[0]][cd1[1]] = ' '
			self.board[cd2[0]][cd2[1]] = ' '
			return True
		return False

	def display_board(self, message: str = None, is_err: str = None, last_duration: str = None, all_informations: bool = False):
		# os.system("clear")
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
		print()


	def opening_standard(self):
		pass
	def opening_pro(self):
		pass
	def opening_swap(self):
		pass
	def opening_swap2(self):
		pass

	def handle_opening(self, opening: str):
		if opening == "pro":
			self.opening_pro()
		elif opening == "swap":
			self.opening_swap()
		elif opening == "swap2":
			self.opening_swap2()

	def read_a_game(self, n: int, stop_read: int):
		filename = f"./game_history/game_{n}.log"
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
			# print(f"{player} : {cut_step[-1]}")
			if player != self.player_turn:
				self.switch_player_turn()
			self.place_stone(cut_step[-1])
			self.switch_player_turn()
		# print(all_steps)

	def play(self, opening: str = "standard"):
		from gomoku_algorithm import minimax

		is_err = False
		message = None
		last_duration = None
		self.handle_opening(opening)
		while terminate_state(self.board, self.black_capture, self.white_capture, self.settings) == False:
			is_err = False
			message = f"Is {'black' if self.get_player_turn() == 'B' else 'white'} player turn."
			self.display_board(message=message, last_duration=last_duration, is_err=is_err)
			if self.get_player_turn() == "B": # Black turn, so player turn
				# mt = MeasureTime(start=True)
				log_mt = MeasureTime(start=True)
				while True:
					user_placement = input(f"{'Black' if self.get_player_turn() == 'B' else 'White'} Turn -> ")
					try:
						self.place_stone(user_placement)
						log_str_time = log_mt.stop(get_str=True, duration_only=True)

						if self.save_game:
							logging.info(f"{log_str_time.ljust(12)} - Player    :{self.get_player_turn()} -> Move:{user_placement}")

						self.switch_player_turn()
						break
					except Exception as e:
						message = str(e)
						is_err = True
						self.display_board(message=message, is_err=is_err)
				last_duration = None
				# self.display_board(message=message, last_duration=last_duration, is_err=is_err)
				# exit(1)
				# last_duration = mt.stop(get_str=True)

			elif self.get_player_turn() == "W": # IA or 2 players turn
				if self.IA == True:
					# Handle IA
					# littleGomoku = c
					mt = MeasureTime(start=True)
					score, move = minimax(convert_to_little_gomoku(self), MAX_DEPTH=3)
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
						# print(score)
						exit(1)
				else:
					log_mt = MeasureTime(start=True)
					while True:
						user_placement = input(f"{'Black' if self.get_player_turn() == 'B' else 'White'} Turn -> ")
						try:
							self.place_stone(user_placement)

							log_str_time = log_mt.stop(get_str=True, duration_only=True)

							if self.save_game:
								logging.info(f"{log_str_time.ljust(12)} - Player    :{self.get_player_turn()} -> Move:{user_placement}")

							self.switch_player_turn()
							break
						except Exception as e:
							message = str(e)
							is_err = True
							self.display_board(message=message, is_err=is_err)
			else:
				raise GomokuError("Player turn error")

		if self.settings.allowed_capture:
			has_winner, who_win = winner_found(self.board)
		else:
			has_winner, who_win = critical_situation(self.board)
		is_err = False
		if has_winner:
			message = f"{'White' if who_win == 'W' else 'Black'} has won the game !"
		else:
			message = "No one has won. It's a perfect tie !"
		self.display_board(message=message, is_err=is_err)


if __name__ == "__main__":
	from gomoku_algorithm import minimax
	from gomoku_heuristic_function import game_state
	SIMULATION = False
	if SIMULATION:
		# settings = GomokuSettings(allowed_capture=False, allowed_win_by_capture=False, allowed_double_three=True)
		go_simulate = Gomoku()
		# go_simulate.read_a_game(3, -2)
		go_simulate.read_a_game(4, -4)

		# LEFT
		# go_simulate.place_stone("h7", "W")
		# go_simulate.place_stone("j8", "B")
		# go_simulate.place_stone("j7", "W")
		# go_simulate.switch_player_turn()


		# RIGHT
		# go_simulate.place_stone("j8", "W")
		# go_simulate.place_stone("f8", "B")
		# go_simulate.place_stone("e8", "W")
		# go_simulate.switch_player_turn()




		# go_simulate.read_a_game(2, -5)
		print(go_simulate)
		print(go_simulate.settings.allowed_capture)
		print(go_simulate.settings.allowed_win_by_capture)
		print(go_simulate.settings.allowed_double_three)
		print(go_simulate.player_turn)
		print(go_simulate.maximizing_player)
		print(go_simulate.minimizing_player)


		littleGomoku = convert_to_little_gomoku(go_simulate)
		result = minimax(littleGomoku, MAX_DEPTH=3)
		# littleGomoku.paint_actions(littleGomoku.get_actions())
		print(littleGomoku)
		# print(game_state(littleGomoku, True))
		print(result)
		go_simulate.play()
	else:
		settings = GomokuSettings(allowed_capture=True, allowed_win_by_capture=True, allowed_double_three=True)
		gomoku = Gomoku(IA=True, who_start="B", save_game=True, settings=settings)
		gomoku.play()



	# PAIRS TO BROKE
	# gomoku.place_stone("B2", "B")
	# gomoku.place_stone("C3", "B")
	# gomoku.place_stone("E6", "B")
	# gomoku.place_stone("E7", "B")
	# gomoku.place_stone("O7", "B")

	# gomoku.place_stone("D3", "W")
	# gomoku.place_stone("H3", "W")
	# gomoku.place_stone("I4", "W")
	# gomoku.place_stone("I5", "W")
	# gomoku.place_stone("H10", "W")

	# ###########
	# gomoku.place_stone("B2", "B")
	# gomoku.place_stone("C3", "B")
	# gomoku.place_stone("D5", "B")
	# gomoku.place_stone("E5", "B")
	# gomoku.place_stone("F6", "B")

	# gomoku.place_stone("D3", "W")
	# gomoku.place_stone("H3", "W")
	# gomoku.place_stone("I4", "W")
	# gomoku.place_stone("I5", "W")
	# gomoku.place_stone("H10", "W")


	# gomoku.place_stone("D4", "B")

	# gomoku.place_stone("L11", "W")

	# gomoku.place_stone("b2", "B")
	# gomoku.place_stone("m4", "W")
	# gomoku.place_stone("c3", "B")
	# gomoku.place_stone("h3", "W")
	# gomoku.place_stone("E6", "B")
	# gomoku.place_stone("h8", "W")
	# gomoku.place_stone("E7", "B")
	# print(gomoku)


	# gomoku.place_stone("E2", "B")
	# gomoku.place_stone("E10", "W")
	# gomoku.play()
	# t = 3
	# for i in range(10):
	# 	if i % 2 == 0:
	# 		gomoku.place_stone(f"C:{t}")
	# 		t += 1
	# 	else:
	# 		gomoku.place_stone(f"I:{i + 1}")
	# print()
	# gomoku.place_stone("D3")
	# gomoku.place_stone("D3")
	# gomoku.place_stone("D4")
	# gomoku.place_stone("D5")
	# gomoku.place_stone("D6")
	# gomoku.place_stone("D7")
	# gomoku.place_stone("Z0")
	# gomoku.place_stone((3, 2))
	# gomoku.place_stone((3, 3))
	# gomoku.place_stone((3, 4))
	# gomoku.place_stone((3, 5))
	# gomoku.place_stone((3, 6))
	# print(gomoku)
	# print(gomoku.get_player_turn())


