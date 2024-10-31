import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_evaluation import pair_can_be_capture
import pprint

board = [
	[" ", "C", " ", " ", " ", " ", " ", " "],
	["W", " ", " ", "W", " ", " ", "W", " "],
	[" ", "A", " ", "E", " ", "C", " ", " "],
	[" ", " ", "A", "E", "C", " ", " ", " "],
	["W", "I", "I", "W", "F", "F", "W", " "],
	[" ", " ", "H", "G", "D", " ", " ", " "],
	[" ", "H", " ", "G", " ", "D", " ", " "],
	["W", " ", " ", "W", " ", " ", "W", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
]

def get_all_positions_pairs(board, i, j):
	all_positions = []
	try: # F
		all_positions.append("".join([board[i][j + k] for k in range(4)]))
	except:
		pass
	try: # I
		all_positions.append("".join([board[i][j - k] for k in range(4)]))
	except:
		pass
	try: # G
		all_positions.append("".join([board[i + k][j] for k in range(4)]))
	except:
		pass
	try: # E
		all_positions.append("".join([board[i - k][j] for k in range(4)]))
	except:
		pass
	try: # A
		all_positions.append("".join([board[i - k][j - k] for k in range(4)]))
	except:
		pass
	try: # D
		all_positions.append("".join([board[i + k][j + k] for k in range(4)]))
	except:
		pass
	try: # C
		all_positions.append("".join([board[i - k][j + k] for k in range(4)]))
	except:
		pass
	try: # H
		all_positions.append("".join([board[i + k][j - k] for k in range(4)]))
	except:
		pass
	return all_positions

pprint.pprint(board) # 4,3

print(get_all_positions_pairs(board, 4, 3))
