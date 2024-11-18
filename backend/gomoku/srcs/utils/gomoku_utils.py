import string
import re
from utils.little_gomoku_utils import get_actions_range

def convert_coordinate_to_xy(coordinate: str) -> tuple[int] | None:
	regex = r"(?:(?:(?P<y>[a-zA-Z])(?P<x>\d+))|(?:(?P<x_alt>\d+)(?P<y_alt>[a-zA-Z])))$"
	match_coordinate = re.match(regex, coordinate)
	if match_coordinate:
		x = match_coordinate.group("x") or match_coordinate.group("x_alt")
		y = match_coordinate.group("y") or match_coordinate.group("y_alt")
		if y.islower():
			y = string.ascii_lowercase.find(y)
		else:
			y = string.ascii_uppercase.find(y)
		return (int(x) - 1, int(y))
	else:
		# print("Not found.")
		return (None, None)

def convert_xy_to_coordinate(x: int, y: int): # x = j | y = i
	try:
		y_str = string.ascii_uppercase[y]
		x_str = str(x + 1)
	except:
		return None
	return (f"{y_str}{x_str}")

def calcul_distance_between_two_points(point1: tuple[int, int], point2: tuple[int, int]) -> float:
	# d = √(x2 - x1)**2 + (y2 - y1)**2|
	v1 = (point1[0] - point2[0]) ** 2
	v2 = (point1[1] - point2[1]) ** 2
	return (v1 + v2) ** 0.5

def opening_pro_get_actions(board: list[list[str]]) -> list[tuple[int]]:
	actions = []
	for i in range(len(board)):
		for j in range(len(board[i])):
			# (9, 9) = Center of the board
			if 4 > calcul_distance_between_two_points((i, j), (9, 9)) > 2 and board[i][j] == " ":
				actions.append((i, j))
	return actions

def opening_swap_get_actions(board: list[list[str]]) -> list[tuple[int]]:
	actions = []
	range_i, range_j = get_actions_range(board)
	if range_i is None or range_j is None:
			range_i = range(7, 12)
			range_j = range(7, 12)
	for i in range_i:
		for j in range_j:
			if board[i][j] == " ":
				actions.append((i, j))
	return actions

if __name__ == "__main__":
	# convert_coordinate_to_xy("D3")
	# convert_coordinate_to_xy("D33")
	# convert_coordinate_to_xy("3D")
	# convert_coordinate_to_xy("3:D")
	print(calcul_distance_between_two_points((0, 1), (-1, 3)))
	# print(convert_xy_to_coordinate(3, 5))

