import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gomoku_utils import *

def test_convert_coordinate_valid():
	assert convert_coordinate("D3") == (2, 3)
	assert convert_coordinate("3D") == (2, 3)
	assert convert_coordinate("E3") == (2, 4)
	assert convert_coordinate("3E") == (2, 4)
	assert convert_coordinate("d3") == (2, 3)
	assert convert_coordinate("3d") == (2, 3)
	assert convert_coordinate("e3") == (2, 4)
	assert convert_coordinate("3e") == (2, 4)

def test_invalid_convert_coordinate():
	assert convert_coordinate("E:3") == (None, None)
	assert convert_coordinate("E:3:3") == (None, None)
	assert convert_coordinate("E3:3") == (None, None)
	assert convert_coordinate(":3") == (None, None)
	assert convert_coordinate(":D") == (None, None)
	assert convert_coordinate("3eeee") == (None, None)
	assert convert_coordinate("-333e") == (None, None)
