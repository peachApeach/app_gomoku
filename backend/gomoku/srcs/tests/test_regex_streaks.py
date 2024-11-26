import re

# r1 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}[^B]))"
# r2 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}[^B]))"
# r3 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}[^B]?))$"
# r4 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}[^B]?))$"


r1 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}(?:(?:\s)|(?:[W]))))"
r2 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}(?:(?:\s)|(?:[W]))))"
r3 = r"(?:\s?[B]{2,}\s?(?:[B]{1,2}(?:(?:\s)|(?:[W]))?))$"
r4 = r"(?:\s?[B]{1,2}\s?(?:[B]{2,}(?:(?:\s)|(?:[W]))?))$"


pattern = rf"{r1}|{r2}|{r3}|{r4}"
mtch = re.findall(rf"{r1}|{r2}", "B BBB BBBB BBBB BBB BB ")

def test_expect_regex():
	assert re.findall(pattern, "B BBB BBBB BBBB BBB BB ") == ['B BBB ', 'BBBB ', 'BBBB ', 'BBB BB ']
	assert re.findall(pattern, "B  BBBB ") == [' BBBB ']
	assert re.findall(pattern, "BB BBB") == ['BB BBB']
	assert re.findall(pattern, "BBB BB BB BBB") == ['BBB BB ', 'BB BBB']
	assert re.findall(pattern, "B BBBB ") == ['B BBBB ']
	assert re.findall(pattern, "BBBB W ") == ['BBBB ']
	assert re.findall(pattern, "BBBB  BBBB") == ['BBBB ', ' BBBB']
	assert re.findall(pattern, "BBBB") == ['BBBB']
	assert re.findall(pattern, " BBBB ") == [' BBBB ']
	assert re.findall(pattern, " BBB BB BBBB ") == [' BBB BB ', 'BBBB ']
	assert re.findall(pattern, " BBB BBWBBBB ") == [' BBB BBW', 'BBBB ']
	assert re.findall(pattern, " BBB BBWBBBB") == [' BBB BBW', 'BBBB']
	assert re.findall(pattern, " BB BBBWBBBB") == [' BB BBBW', 'BBBB']
	assert re.findall(pattern, "WBB BBBW BBBB ") == ['BB BBBW', ' BBBB ']
