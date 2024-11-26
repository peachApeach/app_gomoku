import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.handle_alignment import adjust_list

def test_adjust_list():
	assert adjust_list(["WWW ", "WWW ", " WWWW", "WWWW"]) == ["WWW ", " WWW ", "  WWWW", "WWWW"]
	assert adjust_list([]) == []
	assert adjust_list(["WWWW"]) == ["WWWW"]
	assert adjust_list(["", "WWWW"]) == ["", "WWWW"]
