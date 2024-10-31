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
from gomoku_evaluation import *
from my_utils import print_error


def print_state():
	pass

class GomokuError(Exception):
	pass

class PlacementError(Exception):
	pass

class Gomoku:
	def __init__(self, board_size: tuple[int] = (14, 14), IA: bool = True, IA_suggestion: bool = False):
		self.IA = IA
		self.IA_suggestion = IA_suggestion
		self.__board_width = board_size[0]
		self.__board_height = board_size[1]
		self.board = [[" " for _ in range(self.__board_width)] for __ in range(self.__board_height)]
		# print(self.board)

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
					content += f"{BLUEB}  {RESET} "
				elif char == 'W':
					content += f"{WHITEHB}  {RESET} "
				else:
					content += f"{BLACKHB}  {RESET} "

			content += "\n\n"
		return content

	def get_player_turn(self) -> str:
		black_stone = 0
		white_stone = 0
		for i in range(self.__board_height):
			for j in range(self.__board_width):
				if self.board[i][j] == 'B':
					black_stone += 1
				elif self.board[i][j] == 'W':
					white_stone += 1
		return 'B' if black_stone == white_stone else 'W'

	# def terminate_state(self, board)

	def place_stone(self, coordinate: str, stone: str = None):
		x, y = convert_coordinate(coordinate)
		if x is None or y is None:
			raise PlacementError("Your coordinates are in invalid format. Except: 'LETTERS:NUMBER'")
			print("Invalid placement format.")
			return False

		if x < 0 or x >= self.__board_width or y < 0 or y >= self.__board_height:
			raise PlacementError("Your coordinates is out of the board.")
			print("Coordinates out of range")
			return
		if self.board[y][x] == ' ':
			self.board[y][x] = self.get_player_turn() if stone == None else stone
			return
			# return True
		else:
			raise PlacementError("This slot is already use. Please choose an other.")
			print("This slot is already use. Please choose an other.")
			return False
		# print(f"x:{x}, y:{y}")

	def display_board(self, message: str = None, is_err: str = False):
		os.system("clear")
		if (message != None):
			print()
			if is_err:
				print(f"{BHRED} ==== ERROR : {message} ===={RESET}")
			else:
				print(f"{BHWHITE} ==== STATE : {message} ===={RESET}")
		print(self)

	def play(self):
		is_err = False
		message = None
		while terminate_state(self.board) == False:
			is_err = False
			message = f"Is {'black' if self.get_player_turn() == 'B' else 'white'} player turn."
			self.display_board(message=message, is_err=is_err)
			if self.get_player_turn() == "B": # Black turn, so player turn
				while True:
					user_placement = input(f"{'black' if self.get_player_turn() == 'B' else 'white'} Turn -> ")
					try:
						self.place_stone(user_placement)
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
						user_placement = input(f"{'black' if self.get_player_turn() == 'B' else 'white'} Turn -> ")
						try:
							self.place_stone(user_placement)
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
			message = f"{'White' if self.get_player_turn() == 'B' else 'Black'} has won the game !"
		else:
			message = "No one has won. It's a perfect tie !"
		self.display_board(message=message, is_err=is_err)


if __name__ == "__main__":
	gomoku = Gomoku(IA=False, board_size=(6, 6))
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


