def get_line_horizontal(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""
	min_j = params_j - radius
	if min_j < 0:
		min_j = 0
	max_j = params_j + (radius + 1)
	if max_j > len(board[params_i]):
		max_j = len(board[params_i])

	for j in range(min_j, max_j):
		line += board[params_i][j]
	return line

def get_line_vertical(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""
	min_i = params_i - radius
	if min_i < 0:
		min_i = 0
	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	for i in range(min_i, max_i):
		line += board[i][params_j]
	return line

def get_line_diagonal_1(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""

	i_radius = 0
	min_i = params_i
	min_j = params_j

	while i_radius < radius and min_i > 0 and min_j > 0:
		min_i -= 1
		min_j -= 1
		i_radius += 1

	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	max_j = params_j + (radius + 1)
	if max_j > len(board[params_i]):
		max_j = len(board[params_i])

	for i, j in zip(range(min_i, max_i), range(min_j, max_j)):
		line += board[i][j]
	return line

def get_line_diagonal_2(board: list[list[str]], params_i: int, params_j: int, radius: int = 4):
	line = ""

	i_radius = 0
	min_i = params_i
	min_j = params_j

	while i_radius < radius and min_i > 0 and min_j < len(board[params_i]) - 1:
		min_i -= 1
		min_j += 1
		i_radius += 1

	max_i = params_i + (radius + 1)
	if max_i > len(board):
		max_i = len(board)

	max_j = params_j - radius
	if max_j < 0:
		max_j = 0

	for i, j in zip(range(min_i, max_i), range(min_j, max_j - 1, -1)):
		line += board[i][j]
	return line
