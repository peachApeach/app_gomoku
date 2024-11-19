from rules.gomoku_rules import switch_opponent


def check_alignment(row: list[str], stone: str, stone_count: int) -> bool:
	return row.count(stone) == stone_count and row.count(" ") == len(row) - stone_count
	pass

def type_of_alignment(row: list[str], stone: str):
	opponent_stone = switch_opponent(stone)
	opponent_count = row.count(opponent_stone)
	if opponent_count > 1:
		return 'invalid', 0
	if opponent_count == 1:
		if row[0] != opponent_stone and row[-1] != opponent_stone:
			return 'invalid', 0
	if row[0] == " " and row[-1] == " ":
		return 'free', row.count(stone)
	else:
		return 'align', row.count(stone)

def is_three_aligned(board: list[list[str]], i, j, stone):
	count = 0

	try: # F
		if check_alignment("".join([board[i][j + k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # G
		if check_alignment("".join([board[i + k][j] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # D
		if check_alignment("".join([board[i + k][j + k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	try: # H
		if check_alignment("".join([board[i + k][j - k] for k in range(1, 6)]), stone, 3):
			count += 1
	except:
		pass
	return count

"""
Si la couleur inverse de la stone (X -> Y) est au bord et unique, c'est un FREE, sinon c'est juste un alignment.
Suffit ensuite de cote la repetition pour savoir si c'est un FOUR, THREE
range(6)
FREE FOUR
- ' XXXX '
- '  XXXX'
FOUR ALIGNED
- ' XXXXY'
- 'YXXXX '
FREE THREE
- ' XX X '
- ' XXX  '
- ...
THREE ALIGNED
- ' XX XY'
- ' XXX Y'
- ...

UNKNOWN THREE
- '  XX X'
- '   XXX'

"""
