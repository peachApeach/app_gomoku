import time
from Colors import *

class MeasureTime:
	def __init__(self):
		self.t_start = None
		self.t_end = None

	def __str__(self) -> str:
		if self.t_end is None:
			return "The timer is not ended."
		else:
			return f"Duration : {self.t_end // 1000000}ms"
	def start(self):
		self.t_start = time.perf_counter_ns()

	def stop(self):
		if self.t_start is None:
			print("The timer has not started yet.")
		else:
			self.t_end = time.perf_counter_ns() - self.t_start
			self.t_start = None
			print(f"{BHWHITE}Duration : {CYANHB}{BHBLACK}{self.t_end // 1000000}ms{RESET}")

if __name__ == "__main__":
	measureTime = MeasureTime()
	measureTime.start()
	time.sleep(0.12)
	measureTime.stop()
