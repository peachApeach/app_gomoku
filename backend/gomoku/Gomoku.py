# The black pieces starts first
# To win : Get 5 pieces in a row : Vertical, Horizontal, Diagonal
# In some rules, this line must be exactly five stones long; six or more stones in a row does not count as a win and is called an overline. : In the context of this
# projet, we will consider 5 or more to be a win.
# If the board is completely filled and no one has made a line of 5 stones, then the game ends in a draw.
# Gomoku will be played on a 19x19 Goban, without limit to the number of stones.
# Swap2 opening
# https://en.wikipedia.org/wiki/Gomoku#Variants

from Colors import *

class Gomoku:
	def __init__(self):
		self.__board_width = 14
		self.__board_height = 14
		self.board = [["*" for _ in range(self.__board_width)] for __ in range(self.__board_height)]
		# print(self.board)

	def __str__(self) -> str:
		content = ""
		for line in self.board:
			for char in line:
				if char == 'B':
					content += f"{BLACKHB} {RESET} "
				elif char == 'W':
					content += f"{WHITEHB} {RESET} "
				else:
					content += f"{YELLOWB} {RESET} "

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

	def place_stone(self, coordinate: tuple[int]):
		self.board[coordinate[0]][coordinate[1]] = self.get_player_turn()
		pass

if __name__ == "__main__":
	gomoku = Gomoku()
	gomoku.place_stone((3, 2))
	print(gomoku)
	print(gomoku.get_player_turn())


