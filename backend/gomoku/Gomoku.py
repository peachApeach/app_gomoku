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
from gomoku_utils import convert_coordinate

class GomokuError(Exception):
	pass

class PlacementError(Exception):
	pass

class Gomoku:
	def __init__(self):
		self.__board_width = 14
		self.__board_height = 14
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
					content += f"{REDHB}  {RESET} "
				elif char == 'W':
					content += f"{CYANHB}  {RESET} "
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


	def place_stone(self, coordinate: str):
		x, y = convert_coordinate(coordinate)
		if x is None or y is None:
			# raise PlacementError("Your coordinates are in invalid format. Except: 'LETTERS:NUMBER'")
			print("Invalid placement format.")
			return

		if x < 0 or x >= self.__board_width or y < 0 or y >= self.__board_height:
			# raise PlacementError("Your coordinates is out of the board.")
			print("Coordinates out of range")
			return
		if self.board[y][x] == ' ':
			self.board[y][x] = self.get_player_turn()
		else:
			# raise PlacementError("This slot is already use. Please choose an other.")
			print("This slot is already use. Please choose an other.")
			return
		# print(f"x:{x}, y:{y}")


if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.place_stone("")
	gomoku.place_stone("D:3")
	gomoku.place_stone("D:3")
	gomoku.place_stone("D:4")
	gomoku.place_stone("D:5")
	gomoku.place_stone("D:6")
	gomoku.place_stone("D:7")
	gomoku.place_stone("Z:0")
	# gomoku.place_stone((3, 2))
	# gomoku.place_stone((3, 3))
	# gomoku.place_stone((3, 4))
	# gomoku.place_stone((3, 5))
	# gomoku.place_stone((3, 6))
	print(gomoku)
	# print(gomoku.get_player_turn())


