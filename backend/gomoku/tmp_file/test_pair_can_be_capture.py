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
	possibility = ["WBBW", "BWWB"]
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
	return all_positions

pprint.pprint(board) # 4,3

print(get_all_positions_pairs(board, 4, 3))
