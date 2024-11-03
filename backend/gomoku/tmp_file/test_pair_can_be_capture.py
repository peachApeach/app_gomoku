import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_rules import pair_can_be_capture
import pprint

board = [
	[" ", "C", " ", " ", " ", " ", " ", " "],
	["W", " ", " ", "W", " ", " ", "W", " "],
	[" ", "A", " ", "E", " ", "B", " ", " "],
	[" ", " ", "A", "E", "B", " ", " ", " "],
	["W", "I", "I", "W", "F", "F", "W", " "],
	[" ", " ", "H", "G", "D", " ", " ", " "],
	[" ", "H", " ", "G", " ", "D", " ", " "],
	["W", " ", " ", "W", " ", " ", "W", " "],
	[" ", " ", " ", " ", " ", " ", " ", " "],
]

def get_all_positions_pairs(board, i, j):
	possibility = ("WBBW", "BWWB")
	try: # F
		if "".join([board[i][j + k] for k in range(4)]) in possibility:
			return [(i, j + 1), (i, j + 2)]
	except:
		pass
	try: # I
		if "".join([board[i][j - k] for k in range(4)]) in possibility:
			return [(i, j - 1), (i, j - 2)]
	except:
		pass
	try: # G
		if "".join([board[i + k][j] for k in range(4)]) in possibility:
			return [(i + 1, j), (i + 2, j)]
	except:
		pass
	try: # E
		if "".join([board[i - k][j] for k in range(4)]) in possibility:
			return [(i - 1, j), (i - 2, j)]
	except:
		pass
	try: # A
		if "".join([board[i - k][j - k] for k in range(4)]) in possibility:
			return [(i - 1, j - 1), (i - 2, j - 2)]
	except:
		pass
	try: # D
		if "".join([board[i + k][j + k] for k in range(4)]) in possibility:
			return [(i + 1, j + 1), (i + 1, j + 2)]
	except:
		pass
	try: # C
		if "".join([board[i - k][j + k] for k in range(4)]) in possibility:
			return [(i - 1, j + 1), (i - 1, j + 2)]
	except:
		pass
	try: # H
		if "".join([board[i + k][j - k] for k in range(4)]) in possibility:
			return [(i + 1, j - 1), (i + 2, j - 2)]
	except:
		pass
	return None

pprint.pprint(board) # 4,3

print(get_all_positions_pairs(board, 4, 3))
