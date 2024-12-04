from rules.GomokuSettings import GomokuSettings
from GomokuState import GomokuState
from utils.little_gomoku_utils import get_actions_range, is_useful_placement
from rules.gomoku_rules import *
from algorithms.gomoku_state import *
from Gomoku import Gomoku, PlacementError
from algorithms.handle_alignment import count_all_alignment, get_score_from_alignment
from utils.Colors import *
import string
import copy
import time
import os
import random
from threading import Thread
import multiprocessing

class LittleGomoku:

	def __init__(
		self, board: list[list[str]], player_turn: str, gomoku_settings: GomokuSettings, max_player: str, min_player: str, black_capture: int, white_capture: int,
		five_aligned_black: int,
		five_aligned_white: int,
		free_three_black: int,
		free_three_white: int,
		free_four_black: int,
		free_four_white: int,
		three_aligned_black: int,
		three_aligned_white: int,
		four_aligned_black: int,
		four_aligned_white: int,

		board_width: int = 19, board_height: int = 19):

		self.board = board
		self.settings = gomoku_settings
		self.player_turn = player_turn
		self.maximizing_player = max_player
		self.minimizing_player = min_player
		self.__board_width = board_width
		self.__board_height = board_height

		self.minimax_node = 0
		# For heuristic function
		self.black_capture = black_capture
		self.white_capture = white_capture

		self.three_aligned_black = three_aligned_black
		self.three_aligned_white = three_aligned_white

		self.four_aligned_black = four_aligned_black
		self.four_aligned_white = four_aligned_white

		self.free_three_black = free_three_black
		self.free_three_white = free_three_white

		self.free_four_black = free_four_black
		self.free_four_white = free_four_white

		self.five_aligned_black = five_aligned_black
		self.five_aligned_white = five_aligned_white

		self.minimax_start = None
		self.minimax_timeout = 5


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
					content += f"{REDHB}{char}{RESET} "
			content += "\n\n"
		return content


	def switch_player_turn(self):
		self.player_turn = 'B' if self.player_turn == 'W' else 'W'

	def place_stone(self, i: int, j: int, stone: str = None):

		if j < 0 or j >= self.__board_width or i < 0 or i >= self.__board_height:
			raise PlacementError("Your coordinates is out of the board.")

		if self.board[i][j] == ' ' or stone == ' ':
			to_place = self.player_turn if stone == None else stone
			if self.settings.allowed_capture == True:
				pairs_captured = pair_can_be_capture(self.board, i, j, to_place)
			else:
				pairs_captured = []

			before_placement_alignment = count_all_alignment(self.board, i, j)
			self.board[i][j] = to_place
			if pairs_captured != []:
				for pair in pairs_captured:
					cd1 = pair[0]
					cd2 = pair[1]
					self.board[cd1[0]][cd1[1]] = ' '
					self.board[cd2[0]][cd2[1]] = ' '

				opponent_stone = switch_opponent(to_place)
				situation = critical_situation(self.board, observed_stone=opponent_stone)
				if situation[0] == True:
					if situation[1] != to_place:
						for pair in pairs_captured:
							cd1 = pair[0]
							cd2 = pair[1]
							self.board[cd1[0]][cd1[1]] = opponent_stone
							self.board[cd2[0]][cd2[1]] = opponent_stone


						self.board[i][j] = ' '
						raise PlacementError("You are in a critical situation. Please fix this !")

				if self.board[i][j] == 'B':
					self.black_capture += len(pairs_captured)
				else:
					self.white_capture += len(pairs_captured)

				after_placement_alignment = count_all_alignment(self.board, i, j)
			else:
				if self.settings.allowed_capture:
					opponent_stone = switch_opponent(to_place)
					situation = critical_situation(self.board, observed_stone=opponent_stone)
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

		self.five_aligned_black += after_placement_alignment['five_aligned_black'] - before_placement_alignment['five_aligned_black']
		self.five_aligned_white += after_placement_alignment['five_aligned_white'] - before_placement_alignment['five_aligned_white']



	def get_actions(self) -> list[tuple[int]]:
		slot_useful = []
		range_i, range_j = get_actions_range(self.board)
		if range_i is None or range_j is None:
			range_i = range(8, 11)
			range_j = range(8, 11)

		for i in range_i:
			for j in range_j:
				if self.board[i][j] == " ":
						count_same, count_different = is_useful_placement(self.board, i, j, self.player_turn, 2)
						if count_same > 0 or count_different > 1:
							slot_useful.append((i, j, count_same * 2 + count_different))

		slot_useful.sort(key=lambda x: x[-1], reverse=True)
		final_action = [(i[0], i[1]) for i in slot_useful]

		if len(final_action) != 0:
			return final_action
		list_empty_slot = [(i, j) for i in range(8, 11) for j in range(8, 11) if self.board[i][j] == " "]
		return [random.choice(list_empty_slot)]


	def super_get_actions(self) -> list[tuple[int]]:
		from algorithms.action_optimization import prune_action
		slot_useful = []
		range_i, range_j = get_actions_range(self.board)
		if range_i is None or range_j is None:
			range_i = range(8, 11)
			range_j = range(8, 11)

		for i in range_i:
			for j in range_j:
				if self.board[i][j] == " ":
						count_same, count_different = is_useful_placement(self.board, i, j, self.player_turn, 2)
						if count_same > 0 or count_different > 1:
							slot_useful.append((i, j, count_same * 2 + count_different))

		# list_orientation = False if self.player_turn == self.minimizing_player else True
		slot_useful.sort(key=lambda x: x[-1], reverse=True)
		final_action = [(item[0], item[1]) for item in slot_useful]

		if len(final_action) != 0:
			# return final_action
			return prune_action(self, final_action)

		list_empty_slot = []
		for i in range(8, 11):
			for j in range(8, 11):
				if self.board[i][j] == " ":
						# tmp = self.simulate_action((i, j))
						# list_empty_slot.append((tmp, (i, j)))
					list_empty_slot.append((i, j))
					# except Exception as e:
						# print(f"{i}|{j} : {e}")
		# print(list_empty_slot)
		return [random.choice(list_empty_slot)]


	def ultimate_get_actions(self, IN_RECURSIVE_ACTION: bool = False) -> list[tuple[int]]:
		# from algorithms.__action_optimization import update_action_efficient
		from algorithms.action_optimization import useful_alignment_placement
		from algorithms.gomoku_heuristic_function import game_state
		actions = []

		range_i, range_j = get_actions_range(self.board)
		if range_i is None or range_j is None:
			range_i = range(8, 11)
			range_j = range(8, 11)
		# return [(i, j) for i in range_i for j in range_j if self.board[i][j] == " "]


		# Step 1: We remove isolated stone
		# Step 2: Check efficient of the action and add efficient in all_actions
		mid_efficient_actions = []
		ultra_efficient_actions = []
		opps_mid_efficient_actions = []
		opps_ultra_efficient_actions = []
		for i in range_i:
			for j in range_j:
				if self.board[i][j] == " ":
					# Step2.1: Check stone around
					count_same, count_different = is_useful_placement(self.board, i, j, self.player_turn, 2)
					if count_same > 0 or count_different > 1:
						from utils.gomoku_utils import convert_xy_to_coordinate
						# print(convert_xy_to_coordinate(j, i))
						# Step2.2: Alignment pertinence
						if useful_alignment_placement(littleGomoku=self, i=i, j=j, stone=self.player_turn):
							# print("HERE : ", convert_xy_to_coordinate(j, i))
							try:
								old_game_state = game_state(self)
								gs = self.do_simulation((i, j))
								new_game_state = game_state(self)
								self.undo_simulation(gs)
								# from utils.gomoku_utils import convert_xy_to_coordinate
								# print("MINE", convert_xy_to_coordinate(j, i), new_game_state)
								if old_game_state != new_game_state:
									ultra_efficient_actions.append(((i, j), new_game_state + (count_same * 2 + count_different) * 0.1))
								else:
									mid_efficient_actions.append(((i, j), (count_same * 2 + count_different) * 0.1))
							except Exception as e:
								pass
						else:
							mid_efficient_actions.append(((i, j), (count_same * 2 + count_different) * 0.1))

					if count_different > 0 or count_same > 1:
						if useful_alignment_placement(littleGomoku=self, i=i, j=j, stone=switch_opponent(self.player_turn)):
							try:
								old_game_state = game_state(self)
								gs = self.do_simulation(action=(i, j), opponent_pov=True)
								new_game_state = game_state(self)
								self.undo_simulation(gs)
								from utils.gomoku_utils import convert_xy_to_coordinate
								# print(convert_xy_to_coordinate(j, i), -new_game_state)
								if old_game_state != new_game_state:
									opps_ultra_efficient_actions.append(((i, j), -new_game_state + (count_same + count_different * 2) * 0.1))
								else:
									opps_mid_efficient_actions.append(((i, j), (count_same + count_different * 2) * 0.1))
							except Exception as e:
								pass
						else:
							opps_mid_efficient_actions.append(((i, j), (count_same + count_different * 2) * 0.1))

		# Step 4: Sort by efficient
		list_orientation = False if self.player_turn == self.minimizing_player else True

		mid_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)
		ultra_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)

		# opps_mid_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)
		# opps_ultra_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)

		mid_efficient_actions += opps_mid_efficient_actions
		ultra_efficient_actions += opps_ultra_efficient_actions

		mid_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)
		ultra_efficient_actions.sort(key=lambda x: x[-1], reverse=list_orientation)
		# print(ultra_efficient_actions)
		if ultra_efficient_actions != []:
			all_actions = ultra_efficient_actions
		elif mid_efficient_actions != []:
			if IN_RECURSIVE_ACTION == False:
				for action, _ in mid_efficient_actions:
					gs = self.do_simulation(action=action)
					final_action = self.ultimate_get_actions(IN_RECURSIVE_ACTION=True)
					self.undo_simulation(gs)
					return final_action
			else:
				all_actions = mid_efficient_actions
		else:
			list_empty_slot = []
			for i in range(8, 11):
				for j in range(8, 11):
					if self.board[i][j] == " ":
						list_empty_slot.append((i, j))
			return list_empty_slot

		# Step 5: Clean and return
		actions = list(dict.fromkeys([action_efficient[0] for action_efficient in all_actions]))
		# actions = [action_efficient[0] for action_efficient in all_actions]
		# print("Step 4: ", actions)

		return actions

	def simulate_action(self, action: tuple[int]) -> "LittleGomoku":
		new_little_gomoku = copy.deepcopy(self)
		new_little_gomoku.place_stone(action[0], action[1])
		new_little_gomoku.switch_player_turn()
		return new_little_gomoku

	def do_simulation(self, action: tuple[int], opponent_pov: bool = False) -> GomokuState:
		gomokuState = GomokuState(self, action)
		if opponent_pov == True:
			self.switch_player_turn()

		try:
			self.place_stone(action[0], action[1])
		except Exception as e:
			if opponent_pov == True:
				self.switch_player_turn()
			raise e
		self.switch_player_turn()
		return gomokuState


	def undo_simulation(self, gomokuState: GomokuState):
		for position in gomokuState.saved_position:
			if self.board[position[0]][position[1]] != position[2]:
				self.board[position[0]][position[1]] = position[2]

		self.player_turn = gomokuState.player_turn

		self.black_capture = gomokuState.black_capture
		self.white_capture = gomokuState.white_capture

		self.three_aligned_black = gomokuState.three_aligned_black
		self.three_aligned_white = gomokuState.three_aligned_white

		self.four_aligned_black = gomokuState.four_aligned_black
		self.four_aligned_white = gomokuState.four_aligned_white

		self.free_three_black = gomokuState.free_three_black
		self.free_three_white = gomokuState.free_three_white

		self.free_four_black = gomokuState.free_four_black
		self.free_four_white = gomokuState.free_four_white

		self.five_aligned_black = gomokuState.five_aligned_black
		self.five_aligned_white = gomokuState.five_aligned_white

	def set_minimax_timeout(self, seconds: int = 5):
		self.minimax_start = time.time()
		self.minimax_timeout = seconds

	def is_minimax_timeout(self):
		current_time = time.time()
		if current_time - self.minimax_start > self.minimax_timeout:
			return True
		return False


	def paint_actions(self, actions: list[tuple[int]], char: str = '??', live_visualisation: bool = False, live_speed: float = 0.25):
		for action in actions:
			self.board[action[0]][action[1]] = char
			if live_visualisation == True:
				os.system('clear')
				print(self)
				time.sleep(live_speed)



if __name__ == "__main__":
	from Gomoku import Gomoku
	from algorithms.gomoku_algorithm import minimax, super_minimax
	from utils.MeasureTime import MeasureTime
	gomoku = Gomoku()
	gomoku.place_stone("G6", "B")
	gomoku.place_stone("H7", "W")
	gomoku.place_stone("J3", "B")
	gomoku.place_stone("H8", "W")
	gomoku.place_stone("J8", "B")
	gomoku.place_stone("H9", "W")
	gomoku.place_stone("J10", "B")
	gomoku.place_stone("R17", "W")
	gomoku.place_stone("R18", "B")
	gomoku.switch_player_turn()

	littleGomoku = LittleGomoku(
		board=gomoku.board,
		player_turn=gomoku.player_turn,
		gomoku_settings=gomoku.settings,
		max_player=gomoku.maximizing_player,
		min_player=gomoku.minimizing_player,
		black_capture=gomoku.black_capture,
		white_capture=gomoku.white_capture,
		three_aligned_black=gomoku.three_aligned_black,
		three_aligned_white=gomoku.three_aligned_white,
		free_three_black=gomoku.free_three_black,
		free_three_white=gomoku.free_three_white,
		four_aligned_black=gomoku.four_aligned_black,
		four_aligned_white=gomoku.four_aligned_white,
		free_four_black=gomoku.free_four_black,
		free_four_white=gomoku.free_four_white,
		five_aligned_black=gomoku.five_aligned_black,
		five_aligned_white=gomoku.five_aligned_white,
		board_width=gomoku.get_board_width(),
		board_height=gomoku.get_board_height())

	print(gomoku)
	# gomoku.board[3][1] = "W"
	print(littleGomoku.player_turn)
	print(littleGomoku.maximizing_player)
	print(littleGomoku.minimizing_player)

	# exit(1)

	measureTime = MeasureTime(start=True)
	# actions = littleGomoku.get_actions()
	minimax(littleGomoku, MAX_DEPTH=2)
	measureTime.stop()
	# littleGomoku.paint_actions(actions, True, 0.1)

	# print(littleGomoku)
