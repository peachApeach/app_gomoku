import string
import re

def convert_coordinate(coordinate: str) -> tuple[int] | None:

	# regex = r"([A-Z]:\d+)|(\d+:[A-Z])"
	regex = r"(?:(?:(?P<y>[A-Z])(?P<x>\d+))|(?:(?P<x_alt>\d+)(?P<y_alt>[A-Z])))$"
	match_coordinate = re.search(regex, coordinate)
	if match_coordinate:
		# print(match_coordinate)
		# print(match_coordinate.group("x"))
		# print(match_coordinate.group("y"))
		x = match_coordinate.group("x") or match_coordinate.group("x_alt")
		y = match_coordinate.group("y") or match_coordinate.group("y_alt")
		y = string.ascii_uppercase.find(y)
		# print(f"x:{x}, y:{y}")
		return (int(x) - 1, int(y))
	else:
		# print("Not found.")
		return (None, None)

if __name__ == "__main__":
	convert_coordinate("D3")
	convert_coordinate("D33")
	convert_coordinate("3D")
	convert_coordinate("3:D")
