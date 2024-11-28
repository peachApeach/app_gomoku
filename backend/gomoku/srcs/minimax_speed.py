from Gomoku import Gomoku
from algorithms.gomoku_algorithm import minimax, super_minimax, super_minimax, negamax
from algorithms.gomoku_heuristic_function import game_state
from utils.MeasureTime import MeasureTime
from utils.little_gomoku_utils import convert_to_little_gomoku
from LittleGomoku import LittleGomoku
import time

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

littleGomoku = convert_to_little_gomoku(gomoku=gomoku)

print(gomoku)
# gomoku.board[3][1] = "W"
print(littleGomoku.player_turn)
print(littleGomoku.maximizing_player)
print(littleGomoku.minimizing_player)

# exit(1)

t = 1

MAX_DEPTH = 10

"""
__________________
| DEPTH | Node   |
| 4     | 12673  |
| 6     | 761602 |

"""

# littleGomoku.paint_actions(littleGomoku.get_actions())
# print(littleGomoku)
# exit(1)

if t == 0:
	measureTime = MeasureTime(start=True)
	score, move = minimax(littleGomoku, MAX_DEPTH=MAX_DEPTH)
	print(f"Score : {score} | Move : {move}")
	measureTime.stop()

# time.sleep(0.5)

elif t == 0.5:
	measureTime = MeasureTime(start=True)
	for i in range(12000):
		littleGomoku.super_get_actions()
	measureTime.stop()

elif t == 1:
	measureTime = MeasureTime(start=True)
	score, move = super_minimax(littleGomoku, MAX_DEPTH=MAX_DEPTH)
	print(f"Score : {score} | Move : {move} | Total Node Create {littleGomoku.minimax_node}")
	measureTime.stop()

elif t == -1:
	measureTime = MeasureTime(start=True)
	score, move = negamax(littleGomoku, MAX_DEPTH=MAX_DEPTH)
	print(f"Score : {score} | Move : {move}")
	measureTime.stop()

elif t == 2:
	measureTime = MeasureTime(start=True)
	for i in range(10000):
		littleGomoku.simulate_action((0, 0))
	measureTime.stop()

elif t == -2:
	measureTime = MeasureTime(start=True)
	for i in range(10000):
		lst_state = littleGomoku.do_simulation((0, 0))
		littleGomoku.undo_simulation(lst_state)
	measureTime.stop()

elif t == 3:
	measureTime = MeasureTime(start=True)
	for i in range(1000):
		littleGomoku.super_get_actions()
	measureTime.stop()

elif t == 4:
	measureTime = MeasureTime(start=True)
	for i in range(500):
		actions = littleGomoku.get_actions()
		for action in actions:
			try:
				littleGomoku.simulate_action(action)
			except:
				pass
	measureTime.stop()

elif t == 5:
	measureTime = MeasureTime(start=True)
	for i in range(500):
		actions = littleGomoku.super_get_actions()
		for action in actions:
			pass
	measureTime.stop()

# littleGomoku.paint_actions(littleGomoku.get_actions(), True)
# littleGomoku.player_turn = "B"
# littleGomoku.super_get_actions()
# littleGomoku.paint_actions(littleGomoku.super_get_actions(), True)
