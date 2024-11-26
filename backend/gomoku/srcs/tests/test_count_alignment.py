import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.count_alignment import type_of_alignment


def test_alignment_align_three(): # GOOD
	assert type_of_alignment("WWW      ", "W") == ('align', 3)
	assert type_of_alignment("WWW  ", "W") == ('align', 3)
	assert type_of_alignment("WWW      ", "W") == ('align', 3)
	assert type_of_alignment("    BBB", "B") == ('align', 3)
	assert type_of_alignment("  BBB", "B") == ('align', 3)


def test_alignment_free_three(): # GOOD
	assert type_of_alignment("  WWW ", "W") == ('free', 3)
	assert type_of_alignment("  W WW ", "W") == ('free', 3)
	assert type_of_alignment(" WW W ", "W") == ('free', 3)

def test_alignment_align_four():
	assert type_of_alignment("  WWWW", "W") == ('align', 4)
	assert type_of_alignment("  WWWW", "W") == ('align', 4)
	assert type_of_alignment("WWWW ", "W") == ('align', 4)
	assert type_of_alignment("WWWW    ", "W") == ('align', 4)
	assert type_of_alignment(" WWW W ", "W") == ('align', 4)
	assert type_of_alignment("  W WWW ", "W") == ('align', 4)
	assert type_of_alignment(" WW WW ", "W") == ('align', 4)
	assert type_of_alignment(" WW WWW ", "W") == ('align', 4)
	assert type_of_alignment("       WWW W ", "W") == ('align', 4)
	assert type_of_alignment("      W WWW        ", "W") == ('align', 4)


def test_alignment_free_four():
	assert type_of_alignment("  WWWW ", "W") == ('free', 4)
	assert type_of_alignment(" WWWW  ", "W") == ('free', 4)
	assert type_of_alignment("      WWWW  ", "W") == ('free', 4)
	assert type_of_alignment("  WWWW  ", "W") == ('free', 4)
	assert type_of_alignment("  WWWW W", "W") == ('free', 4)
	assert type_of_alignment("  WWWW W   ", "W") == ('free', 4)
	assert type_of_alignment("W WWWW ", "W") == ('free', 4)
	# assert type_of_alignment("W WWWW", "W") == ('free', 4)


def test_alignment_align_five():
	assert type_of_alignment(" WWWWW ", "W") == ('align', 5)
	assert type_of_alignment(" WWWWWB", "W") == ('align', 5)
	assert type_of_alignment("   WWWWW", "W") == ('align', 5)
	assert type_of_alignment("WWWWW ", "W") == ('align', 5)
	assert type_of_alignment(" WWWWW", "W") == ('align', 5)
	assert type_of_alignment("    WWWWW    ", "W") == ('align', 5)
	assert type_of_alignment("    WWWWWWWWWW    ", "W") == ('align', 5)


# def test_alignment_other():
# 	assert type_of_alignment("    WW", "W") == ('align', 2)
	# assert type_of_alignment("   WWB", "W") == ('invalid', 0)

