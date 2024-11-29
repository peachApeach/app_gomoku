from threading import Thread
import random
import time

# MAX THREADS : cat /proc/sys/kernel/threads-max

print(any([False, False, False]))

def foo(result, index):
	time.sleep(1)
	result[index] = random.randint(0, 100)
	# print(result)

class MainClass:
	def __init__(self):
		pass

	def run(self, nb_threads: int = 5):
		result = [-1] * nb_threads
		all_threads = [None] * nb_threads
		for i in range(nb_threads):
			all_threads[i] = Thread(target=foo, args=(result, i))
			all_threads[i].start()

		# do some other stuff

		for i in range(len(all_threads)):
			all_threads[i].join()

		print(result)



# print(random.randint(0, 20))
# result = [-1] * 10
# print(result)

mainCls = MainClass()
mainCls.run(1000)
