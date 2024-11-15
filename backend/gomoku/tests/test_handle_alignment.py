import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from handle_alignment import alignment_streaks

def test_alignment_streaks():
	"""
	NEED TO RETURN THIS :
	'free_four_black',
	'free_four_white',
	'four_aligned_black',
	'four_aligned_white',
	'free_three_black',
	'free_three_white',
	'three_aligned_black',
	'three_aligned_white',
	"""
	assert alignment_streaks("   BBB WWWW        ") == {
		'free_four_black': 0,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 1,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("   BBB   BB        ") == {
		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 1,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("   BBB   BBB  WWW  ") == {
		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 2,
		'free_three_white': 1,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("   BBB   BBB  WWWW ") == {
		'free_four_black': 0,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 2,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("BBB                ") == {
		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 1,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("BBBB               ") == {
		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 1,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	# assert alignment_streaks("                   ") == {
	# 	'free_four_black': 0,
	# 	'free_four_white': 0,

	# 	'four_aligned_black': 0,
	# 	'four_aligned_white': 0,

	# 	'free_three_black': 0,
	# 	'free_three_white': 0,

	# 	'three_aligned_black': 0,
	# 	'three_aligned_white': 0,
	# }

