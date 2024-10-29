# The black pieces starts first
# To win : Get 5 pieces in a row : Vertical, Horizontal, Diagonal
# In some rules, this line must be exactly five stones long; six or more stones in a row does not count as a win and is called an overline. : In the context of this
# projet, we will consider 5 or more to be a win.
# If the board is completely filled and no one has made a line of 5 stones, then the game ends in a draw.
# Gomoku will be played on a 19x19 Goban, without limit to the number of stones.
# Swap2 opening
# https://en.wikipedia.org/wiki/Gomoku#Variants
import pprint
import string

class Gomoku:
	def __init__(self):
		self.__board_width = 2
		self.__board_height = 9
		self.board = [["*" for _ in range(self.__board_width)] for __ in range(self.__board_height)]
		# print(self.board)

	def __str__(self) -> str:
		content = ""
		for line in self.board:
			for char in line:
				content += f"{char} "
			content += "\n"
		# pprint.pprint(self.board)
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

if __name__ == "__main__":
	gomoku = Gomoku()

	print(gomoku)
	print(gomoku.get_player_turn())

