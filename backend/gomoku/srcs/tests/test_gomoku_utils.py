import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.gomoku_utils import *

def test_valid_convert_coordinate_to_xy():
	assert convert_coordinate_to_xy("D3") == (2, 3)
	assert convert_coordinate_to_xy("3D") == (2, 3)
	assert convert_coordinate_to_xy("E3") == (2, 4)
	assert convert_coordinate_to_xy("3E") == (2, 4)
	assert convert_coordinate_to_xy("d3") == (2, 3)
	assert convert_coordinate_to_xy("3d") == (2, 3)
	assert convert_coordinate_to_xy("e3") == (2, 4)
	assert convert_coordinate_to_xy("3e") == (2, 4)

def test_invalid_convert_coordinate_to_xy():
	assert convert_coordinate_to_xy("E:3") == (None, None)
	assert convert_coordinate_to_xy("E:3:3") == (None, None)
	assert convert_coordinate_to_xy("E3:3") == (None, None)
	assert convert_coordinate_to_xy(":3") == (None, None)
	assert convert_coordinate_to_xy(":D") == (None, None)
	assert convert_coordinate_to_xy("3eeee") == (None, None)
	assert convert_coordinate_to_xy("-333e") == (None, None)

def test_valid_convert_xy_to_coordinate():
	assert convert_xy_to_coordinate(0, 0) == "A1"
	assert convert_xy_to_coordinate(1, 1) == "B2"
	assert convert_xy_to_coordinate(4, 2) == "C5"
	assert convert_xy_to_coordinate(8, 0) == "A9"
	assert convert_xy_to_coordinate(1, 9) == "J2"
	assert convert_xy_to_coordinate(18, 18) == "S19"

def test_invalid_convert_xy_to_coordinate():
	# assert convert_xy_to_coordinate(26, 9) == None
	assert convert_xy_to_coordinate(0, 26) == None
	# assert convert_xy_to_coordinate(0, 19) == None
	# assert convert_xy_to_coordinate(19, 0) == None
