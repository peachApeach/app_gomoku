import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_utils import *

def test_convert_coordinate_valid():
	assert convert_coordinate("D:3") == (3, 3)
	assert convert_coordinate("3:D") == (3, 3)
	assert convert_coordinate("E:3") == (3, 4)
	assert convert_coordinate("3:E") == (3, 4)

def test_invalid_convert_coordinate():
	assert convert_coordinate("E3") == (None, None)
	assert convert_coordinate("E:3:3") == (None, None)
	assert convert_coordinate("E3:3") == (None, None)
	assert convert_coordinate(":3") == (None, None)
	assert convert_coordinate(":D") == (None, None)
