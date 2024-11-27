from Gomoku import Gomoku
from utils.little_gomoku_utils import convert_to_little_gomoku
from LittleGomoku import LittleGomoku
from GomokuState import GomokuState

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

lst_state = []

print(littleGomoku)
lst_state.append(littleGomoku.do_simulation((3, 4)))
print(littleGomoku)
lst_state.append(littleGomoku.do_simulation((3, 5)))
print(littleGomoku)
lst_state.append(littleGomoku.do_simulation((3, 6)))
print(littleGomoku)

while True:
	try:
		last_state = lst_state.pop()
		littleGomoku.undo_simulation(last_state)
		print(littleGomoku)
	except:
		break

# littleGomoku.undo_simulation(gomokuState)

print(littleGomoku)
