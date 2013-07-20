from time import sleep, time 
import random
import pickle
from hue import *

random.seed()
tf = "times.pickle"

try:
	times = pickle.load(open(tf))
except:
	times = {}

for period in frange(0.0, 1.0, 0.05):
	if period not in times:
		times[period] = []
		for i in range(50):
			start = time()
			try:
				rgb(3, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
				end = time()
			except:
				raise
				end = start + 5.0
			times[period].append(end - start)
			print end-start
			sleep(period)
		pickle.dump(times, open(tf, "w"))
		sleep(5.0)

print sorted(times)
