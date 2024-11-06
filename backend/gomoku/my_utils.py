from Colors import *

def print_error(e: Exception):
	print(f"{BHRED}Error{RESET}")
	print(f"{BRED}Name: {type(e).__name__}{RESET}")
	if str(e) != "":
		print(f"{BRED}Message: {e}{RESET}")

if __name__ == "__main__":
	try:
		raise Exception
	except Exception as e:
		print_error(e)
	print()
	try:
		raise Exception("Test")
	except Exception as e:
		print_error(e)
