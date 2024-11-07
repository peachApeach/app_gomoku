from GomokuSettings import GomokuSettings
from gomoku_rules import *
from gomoku_state import *
from Gomoku import *
from Colors import *

class LittleGomoku:

	def __init__(self, board: list[list[str]], player_turn: str, gomoku_settings: GomokuSettings, max_player: str, min_player: str, black_capture: int, white_capture: int, free_three_black: int, free_three_white: int, board_width: int = 19, board_height: int = 19):

		self.board = board
		self.settings = gomoku_settings
		self.player_turn = player_turn
		self.maximizing_player = max_player
		self.minimizing_player = min_player
		self.black_capture = black_capture
		self.white_capture = white_capture
		self.free_three_black = free_three_black
		self.free_three_white = free_three_white
		self.__board_width = board_width
		self.__board_height = board_height


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


	def is_valid_placement(self, i: int, j: int, stone: str = None) -> bool:
		if i is None or j is None:
			return False
		if i < 0 or i >= self.__board_width or j < 0 or j >= self.__board_height:
			return False

		if self.board[i][j] == ' ' or stone == ' ':
			to_place = self.player_turn if stone == None else stone
			if self.settings.allowed_capture == True:
				if pair_can_be_capture(self.board, i, j, to_place):
					return True
				self.board[i][j] = to_place
				situation = critical_situation(self.board)
				if situation[0] == True:
					if situation[1] != to_place:
						self.board[i][j] = ' '
						return False
				self.board[i][j] = ' '
			if self.settings.allowed_double_three == False:
				invalid_free_three = is_creating_free_three(self.board, i, j, to_place)
				return invalid_free_three == False
		else:
			return False
		return True

	def place_stone(self, x: int, y: int, stone: str = None):
		# if x is None or y is None:
		# 	raise PlacementError("Your coordinates are in invalid format. Except: 'LETTERS:NUMBER'")

		# if x < 0 or x >= self.__board_width or y < 0 or y >= self.__board_height:
		# 	raise PlacementError("Your coordinates is out of the board.")

		if stone == " ":
			self.board[y][x] = " "
			return
		# if force:
		# 	self.board[y][x] = self.get_player_turn() if stone == None else stone
		# 	return

		if self.board[y][x] == ' ' or stone == ' ':
			to_place = self.player_turn if stone == None else stone
			if self.settings.allowed_capture == True:
				value = pair_can_be_capture(self.board, y, x, to_place)
			else:
				value = None
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

				if self.settings.allowed_capture:
					situation = critical_situation(self.board)
					if situation[0] == True:
						if situation[1] != to_place:
							# print(to_place)
							self.board[y][x] = ' '
							raise PlacementError("You are in a critical situation. Please fix this !")

				if self.settings.allowed_double_three == False:
					nb_free_three = count_free_three(self.board, to_place)
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
		else:
			raise PlacementError("This slot is already use. Please choose an other.")


	def get_actions(self) -> list[tuple[int]]:
		"""
		Ca renvoie toutes les actions qui ne raise aucune erreur.
		Donc on recupere toutes les cases vides, on les converti en ALPHA:NUM
		Puis on teste de les ajouter et retirer.
		(?) Ne pas tester les cases en dehors d'un rayon de +2/3 du carré former par les pions pour eviter de tester les bords inutiles. (?)
		"""
		empty_slot = []
		# iteration = 0
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
		# for i in range(self.__board_height):
		# 	for j in range(self.__board_width):
				if self.board[i][j] == " ":
					# try:
					if self.is_valid_placement(i=i, j=j):
						empty_slot.append((i, j))
					else:
						print(f"Invalid slot : [{i}]:[{j}]")
					# except Exception as e:
					# 	print(f"Error : ({e}):({i},{j}) : Invalid case. {iteration}")
					# iteration += 1

		return empty_slot

	def simulate_action(self, action: str) -> "LittleGomoku":
		pass


	pass

if __name__ == "__main__":
	pass
