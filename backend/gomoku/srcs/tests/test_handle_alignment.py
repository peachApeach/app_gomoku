import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.handle_alignment import alignment_streaks

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

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
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 1,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  WWWW W            ") == {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  WWWW W") == {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  BBBBB  WWWW     BBBBB       ") == {
		'five_aligned_black': 2,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  BBBBBWWWW BBBBB       ") == {
		'five_aligned_black': 2,
		'five_aligned_white': 0,

		'free_four_black': 0,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 1,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  BBBB BB       ") == {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 1,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  BBBB WWWW       ") == {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 1,
		'free_four_white': 1,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	assert alignment_streaks("  BBBB BBBB       ") == {
		'five_aligned_black': 0,
		'five_aligned_white': 0,

		'free_four_black': 2,
		'free_four_white': 0,

		'four_aligned_black': 0,
		'four_aligned_white': 0,

		'free_three_black': 0,
		'free_three_white': 0,

		'three_aligned_black': 0,
		'three_aligned_white': 0,
	}
	# assert alignment_streaks("                   ") == {
		# 'five_aligned_black': 0,
		# 'five_aligned_white': 0,

	# 	'free_four_black': 0,
	# 	'free_four_white': 0,

	# 	'four_aligned_black': 0,
	# 	'four_aligned_white': 0,

	# 	'free_three_black': 0,
	# 	'free_three_white': 0,

	# 	'three_aligned_black': 0,
	# 	'three_aligned_white': 0,
	# }
	# assert alignment_streaks("                   ") == {
		# 'five_aligned_black': 0,
		# 'five_aligned_white': 0,

	# 	'free_four_black': 0,
	# 	'free_four_white': 0,

	# 	'four_aligned_black': 0,
	# 	'four_aligned_white': 0,

	# 	'free_three_black': 0,
	# 	'free_three_white': 0,

	# 	'three_aligned_black': 0,
	# 	'three_aligned_white': 0,
	# }

