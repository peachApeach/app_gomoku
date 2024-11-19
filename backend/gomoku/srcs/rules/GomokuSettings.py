class GomokuSettings:
	def __init__(self,
	allowed_capture: bool = True,
	allowed_win_by_capture: bool = True,
	allowed_double_three: bool = False
	):
		self.allowed_capture = allowed_capture
		self.allowed_win_by_capture = allowed_win_by_capture
		self.allowed_double_three = allowed_double_three
