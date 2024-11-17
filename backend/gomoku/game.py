#!/bin/python3

from srcs.Gomoku import Gomoku
from srcs.utils.Colors import *
import argparse
import random

def main():
	parser = argparse.ArgumentParser(description="Play Gomoku.")

	parser.add_argument(
		'-p', '--player',
		type=str,
		default=random.choice(['B', 'W'])
	)

	parser.add_argument(
		'-i', '--ia',
		type=int,
		default=1000,
		help=f"The number of iterations the AI will go through to train itself (default: 1000)."
	)
	parser.add_argument(
		'-o', '--opening',
		type=str,
		default="standard",
		help="The learning rate that influences how quickly the model converges (default: 0.01)."
	)
	parser.add_argument(
		'-r', '--ia',
		default=True,
		action='store_true',
		help="Enable animation of the training curves."
	)
	parser.add_argument(
		'-r', '--replay',
		action='store_true',
		help="Enable animation of the training curves."
	)

	args = parser.parse_args()

	try:
		config_file = args.file
		iterations = args.iterations
		learning_rate = args.learning_rate
		replay = args.replay

		linearRegression = Gomoku()
		linearRegression.train_model(
			config_file=config_file,
			iterations=iterations,
			learningRate=learning_rate,
			animate=animate
		)

	except Exception as e:
		error_msg = f"{URED}{BHRED}Error{RESET}\n"
		error_msg += f"{BHRED}Name: {RED}{type(e).__name__}\n"
		error_msg += f"{BHRED}Message: {RED}{e}\n"
		print(error_msg)

if __name__ == "__main__":
	main()
