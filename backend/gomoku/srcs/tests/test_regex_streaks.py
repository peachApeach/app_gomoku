import sys
import os
import re
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from algorithms.GomokuRegex import GomokuRegex

# r1 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}[^B]))"
# r2 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}[^B]))"
# r3 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}[^B]?))$"
# r4 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}[^B]?))$"


# r1 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}(?:(?:\s)|(?:[W]))))"
# r2 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}(?:(?:\s)|(?:[W]))))"
# r3 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}(?:(?:\s)|(?:[W]))?))$"
# r4 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}(?:(?:\s)|(?:[W]))?))$"


pattern = GomokuRegex().black_streaks
# mtch = re.findall(rf"{r1}|{r2}", "B BBB BBBB BBBB BBB BB ")

def test_expect_regex():
	assert re.findall(pattern, "B BBB BBBB BBBB BBB BB ") == ['B BBB ', 'BBBB ', 'BBBB ', 'BBB BB ']
	assert re.findall(pattern, "B  BBBB ") == ['  BBBB ']
	assert re.findall(pattern, "BB BBB") == ['BB BBB']
	assert re.findall(pattern, "BBB BB") == ['BBB BB']
	assert re.findall(pattern, "BBB BB BB BBB") == ['BBB BB ', 'BB BBB']
	assert re.findall(pattern, "B BBBB ") == ['B BBBB ']
	assert re.findall(pattern, "BBBB W ") == ['BBBB ']
	assert re.findall(pattern, "BBBB  BBBB") == ['BBBB  ', 'BBBB']
	assert re.findall(pattern, "BBBB") == ['BBBB']
	assert re.findall(pattern, "BBBB BB") == ['BBBB BB']
	assert re.findall(pattern, " BBBB ") == [' BBBB ']
	assert re.findall(pattern, " BBB BB   BBBB ") == [' BBB BB   ', 'BBBB ']
	assert re.findall(pattern, " BBB BBWBBBB ") == [' BBB BBW', 'BBBB ']
	assert re.findall(pattern, " BBB BBWBBBB") == [' BBB BBW', 'BBBB']
	assert re.findall(pattern, " BB BBBWBBBB") == [' BB BBBW', 'BBBB']
	assert re.findall(pattern, "WBB BBBW BBBB ") == ['BB BBBW', ' BBBB ']
	assert re.findall(pattern, "WBBB BBBW") == ['BBB ', 'BBBW']
	assert re.findall(pattern, "WBBB      W     ") == ['BBB      ']
	assert re.findall(pattern, "BB BBBW") == ['BB BBBW']
	assert re.findall(pattern, "BBB BBW") == ['BBB BBW']
