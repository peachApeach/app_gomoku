import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_line_horizontal(board: list[list[str]], params_i: int, params_j: int, stone: str = None, preshot: bool = False):
	line = ""
	placement_player = None
	for j in range(len(board[params_i])):
		if preshot == True and stone != None and j == params_j:
			placement_player = len(line)
			# board[params_i][j] = stone
			line += stone
		else:
			# board[params_i][j] = "??"
			line += board[params_i][j]
	return line, placement_player

def get_line_vertical(board: list[list[str]], params_i: int, params_j: int, stone: str = None, preshot: bool = False):
	line = ""
	placement_player = None
	for i in range(len(board)):
		if preshot == True and stone != None and i == params_i:
			placement_player = len(line)
			# board[i][params_j] = stone
			line += stone
		else:
			# board[i][params_j] = "??"
			line += board[i][params_j]
	return line, placement_player

def get_line_diagonal_1(board: list[list[str]], params_i: int, params_j: int, stone: str = None, preshot: bool = False):
	line = ""
	placement_player = None


	min_i = params_i
	min_j = params_j

	while min_i > 0 and min_j > 0:
		min_i -= 1
		min_j -= 1

	max_i = len(board)
	max_j = len(board[params_i])

	for i, j in zip(range(min_i, max_i), range(min_j, max_j)):
		if preshot == True and stone != None and i == params_i and j == params_j:
			placement_player = len(line)
			# board[i][j] = stone
			line += stone
		else:
			# board[i][j] = "??"
			line += board[i][j]
	return line, placement_player

def get_line_diagonal_2(board: list[list[str]], params_i: int, params_j: int, stone: str = None, preshot: bool = False):
	line = ""
	placement_player = None

	min_i = params_i
	min_j = params_j

	while min_i > 0 and min_j < len(board[params_i]) - 1:
		min_i -= 1
		min_j += 1

	max_i = len(board)
	max_j = 0

	for i, j in zip(range(min_i, max_i), range(min_j, max_j - 1, -1)):
		if preshot == True and stone != None and i == params_i and j == params_j:
			placement_player = len(line)
			# board[i][j] = stone
			line += stone
		else:
			# board[i][j] = "??"
			line += board[i][j]
	return line, placement_player


if __name__ == "__main__":
	from Gomoku import Gomoku
	gomoku = Gomoku()

	i, j = 14, 14
	get_line_horizontal(gomoku.board, i, j, "XX", preshot=True)
	get_line_vertical(gomoku.board, i, j, "XX", preshot=True)
	get_line_diagonal_1(gomoku.board, i, j, "XX", preshot=True)
	get_line_diagonal_2(gomoku.board, i, j, "XX", preshot=True)

	print(gomoku)


# def get_line_horizontal(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None
# 	min_j = params_j - radius
# 	if min_j < 0:
# 		min_j = 0
# 	max_j = params_j + (radius + 1)
# 	if max_j > len(board[params_i]):
# 		max_j = len(board[params_i])

# 	for j in range(min_j, max_j):
# 		if preshot == True and stone != None and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[params_i][j]
# 	return line, placement_player

# def get_line_vertical(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None
# 	min_i = params_i - radius
# 	if min_i < 0:
# 		min_i = 0
# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	for i in range(min_i, max_i):
# 		if preshot == True and stone != None and i == params_i:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][params_j]
# 	return line, placement_player

# def get_line_diagonal_1(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None

# 	i_radius = 0
# 	min_i = params_i
# 	min_j = params_j

# 	while i_radius < radius and min_i > 0 and min_j > 0:
# 		min_i -= 1
# 		min_j -= 1
# 		i_radius += 1

# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	max_j = params_j + (radius + 1)
# 	if max_j > len(board[params_i]):
# 		max_j = len(board[params_i])

# 	for i, j in zip(range(min_i, max_i), range(min_j, max_j)):
# 		if preshot == True and stone != None and i == params_i and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][j]
# 	return line, placement_player

# def get_line_diagonal_2(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None

# 	i_radius = 0
# 	min_i = params_i
# 	min_j = params_j

# 	while i_radius < radius and min_i > 0 and min_j < len(board[params_i]) - 1:
# 		min_i -= 1
# 		min_j += 1
# 		i_radius += 1

# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	max_j = params_j - radius
# 	if max_j < 0:
# 		max_j = 0

# 	for i, j in zip(range(min_i, max_i), range(min_j, max_j - 1, -1)):
# 		if preshot == True and stone != None and i == params_i and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][j]
# 	return line, placement_player


# def get_line_horizontal(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None
# 	min_j = params_j - radius
# 	if min_j < 0:
# 		min_j = 0
# 	max_j = params_j + (radius + 1)
# 	if max_j > len(board[params_i]):
# 		max_j = len(board[params_i])

# 	for j in range(min_j, max_j):
# 		if preshot == True and stone != None and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[params_i][j]
# 	return line, placement_player

# def get_line_vertical(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None
# 	min_i = params_i - radius
# 	if min_i < 0:
# 		min_i = 0
# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	for i in range(min_i, max_i):
# 		if preshot == True and stone != None and i == params_i:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][params_j]
# 	return line, placement_player

# def get_line_diagonal_1(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None

# 	i_radius = 0
# 	min_i = params_i
# 	min_j = params_j

# 	while i_radius < radius and min_i > 0 and min_j > 0:
# 		min_i -= 1
# 		min_j -= 1
# 		i_radius += 1

# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	max_j = params_j + (radius + 1)
# 	if max_j > len(board[params_i]):
# 		max_j = len(board[params_i])

# 	for i, j in zip(range(min_i, max_i), range(min_j, max_j)):
# 		if preshot == True and stone != None and i == params_i and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][j]
# 	return line, placement_player

# def get_line_diagonal_2(board: list[list[str]], params_i: int, params_j: int, radius: int = 4, stone: str = None, preshot: bool = False):
# 	line = ""
# 	placement_player = None

# 	i_radius = 0
# 	min_i = params_i
# 	min_j = params_j

# 	while i_radius < radius and min_i > 0 and min_j < len(board[params_i]) - 1:
# 		min_i -= 1
# 		min_j += 1
# 		i_radius += 1

# 	max_i = params_i + (radius + 1)
# 	if max_i > len(board):
# 		max_i = len(board)

# 	max_j = params_j - radius
# 	if max_j < 0:
# 		max_j = 0

# 	for i, j in zip(range(min_i, max_i), range(min_j, max_j - 1, -1)):
# 		if preshot == True and stone != None and i == params_i and j == params_j:
# 			placement_player = len(line)
# 			line += stone
# 		else:
# 			line += board[i][j]
# 	return line, placement_player
