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
from gomoku_utils import convert_coordinate
from gomoku_state import *
from gomoku_rules import *
from my_utils import print_error


def print_state():
	pass

class GomokuError(Exception):
	pass

class PlacementError(Exception):
	pass

class Gomoku:
	def __init__(self, board_size: tuple[int] = (14, 14), IA: bool = True, IA_suggestion: bool = False, who_start: str = 'B'):
		self.IA = IA
		self.IA_suggestion = IA_suggestion
		self.__board_width = board_size[0]
		self.__board_height = board_size[1]
		self.black_capture = 0
		self.white_capture = 0
		self.free_three_black = 0
		self.free_three_white = 0
		self.player_turn = who_start
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
				else:
					content += f"{BLACKHB}  {RESET} "

			content += "\n\n"
		return content

	def switch_player_turn(self):
		self.player_turn = 'B' if self.player_turn == 'W' else 'W'

	def get_player_turn(self) -> str:
		return self.player_turn
		# black_stone = 0
		# white_stone = 0
		# for i in range(self.__board_height):
		# 	for j in range(self.__board_width):
		# 		if self.board[i][j] == 'B':
		# 			black_stone += 1
		# 		elif self.board[i][j] == 'W':
		# 			white_stone += 1
		# return 'B' if black_stone == white_stone else 'W'

	def place_stone(self, coordinate: str, stone: str = None):
		x, y = convert_coordinate(coordinate)
		if x is None or y is None:
			raise PlacementError("Your coordinates are in invalid format. Except: 'LETTERS:NUMBER'")

		if x < 0 or x >= self.__board_width or y < 0 or y >= self.__board_height:
			raise PlacementError("Your coordinates is out of the board.")

		if self.board[y][x] == ' ' or stone == ' ':
			to_place = self.get_player_turn() if stone == None else stone
			value = pair_can_be_capture(self.board, y, x, to_place)
			if value:
				self.board[y][x] = to_place
				if self.board[y][x] == 'B':
					self.black_capture += 1
				else:
					self.white_capture += 1
				cd1 = value[0]
				cd2 = value[1]
				self.board[cd1[0]][cd1[1]] = ' '
				self.board[cd2[0]][cd2[1]] = ' '
			else:
				# print(self.free_three_black)
				self.board[y][x] = to_place
				nb_free_three = count_free_three(self.board, to_place)
				# if stone == None:
				# 	os.system('clear')
				# 	print(nb_free_three)
				# 	print(self)
				# 	exit(2)
				if to_place == 'B':
					if nb_free_three - self.free_three_black >= 2:
						self.board[y][x] = ' '
						raise PlacementError("Your coordinates will create a double-three, this is forbidden.")
					else:
						self.free_three_black = nb_free_three
				else:
					if nb_free_three - self.free_three_white >= 2:
						self.board[y][x] = ' '
						raise PlacementError("Your coordinates will create a double-three, this is forbidden.")
					else:
						self.free_three_white = nb_free_three


				# if stone == None:
				# 	raise Exception
				# print(is_creating_double_three(self.board, y, x, to_place))
				# if is_creating_double_three(self.board, y, x, to_place):
				# 	raise PlacementError("This coordinates will create a double-three, it's forbidden.")
				# Check if that create a double three...
		else:
			raise PlacementError("This slot is already use. Please choose an other.")

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

	def display_board(self, message: str = None, is_err: str = False):
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
		print()

	def play(self):
		is_err = False
		message = None
		while terminate_state(self.board, self.black_capture, self.white_capture) == False:
			# if self.remove_pairs() == True:
			# 	continue
			is_err = False
			message = f"Is {'black' if self.get_player_turn() == 'B' else 'white'} player turn."
			self.display_board(message=message, is_err=is_err)
			if self.get_player_turn() == "B": # Black turn, so player turn
				while True:
					user_placement = input(f"{'Black' if self.get_player_turn() == 'B' else 'White'} Turn -> ")
					try:
						self.place_stone(user_placement)
						situation = critical_situation(self.board)
						if situation[0] == True:
							if situation[1] == self.get_player_turn():
								self.place_stone(user_placement, ' ')
								raise PlacementError("You are in a critical situation.")
						self.switch_player_turn()
						break
					except Exception as e:
						message = str(e)
						is_err = True
						self.display_board(message=message, is_err=is_err)
						# print_error(e)

			elif self.get_player_turn() == "W": # IA or 2 players turn
				if self.IA == True:
					# Handle IA
					pass
				else:
					while True:
						user_placement = input(f"{'Black' if self.get_player_turn() == 'B' else 'White'} Turn -> ")
						try:
							self.place_stone(user_placement)
							situation = critical_situation(self.board)
							if situation[0] == True:
								if situation[1] == self.get_player_turn():
									self.place_stone(user_placement, ' ')
									raise PlacementError("You are in a critical situation.")
							self.switch_player_turn()
							break
						except Exception as e:
							message = str(e)
							is_err = True
							self.display_board(message=message, is_err=is_err)
			else:
				raise GomokuError("Player turn error")

		has_winner, who_win = winner_found(self.board)
		is_err = False
		if has_winner:
			message = f"{'White' if who_win == 'W' else 'Black'} has won the game !"
		else:
			message = "No one has won. It's a perfect tie !"
		self.display_board(message=message, is_err=is_err)


if __name__ == "__main__":
	gomoku = Gomoku(IA=False)


	gomoku.place_stone("B2", "B")
	gomoku.place_stone("C3", "B")
	# gomoku.place_stone("D4", "B")
	gomoku.place_stone("D5", "B")
	gomoku.place_stone("E5", "B")
	gomoku.place_stone("F6", "B")

	gomoku.place_stone("D3", "W")
	gomoku.place_stone("H3", "W")
	gomoku.place_stone("I4", "W")
	gomoku.place_stone("I5", "W")
	gomoku.place_stone("H10", "W")

	# gomoku.place_stone("b2", "B")
	# gomoku.place_stone("m4", "W")
	# gomoku.place_stone("c3", "B")
	# gomoku.place_stone("h3", "W")
	# gomoku.place_stone("E6", "B")
	# gomoku.place_stone("h8", "W")
	# gomoku.place_stone("E7", "B")


	# gomoku.place_stone("E2", "B")
	# gomoku.place_stone("E10", "W")
	gomoku.play()
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


