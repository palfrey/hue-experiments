from hue import *
import pickle
from time import sleep
from sys import argv

pixels = pickle.load(open(argv[1]))
period = float(argv[2])

lamps = [int(x) for x in argv[3:]]

if len(lamps) == 0:
	raise Exception, "need some lamps"

while True:
	for pixelSet in pixels:
		for i, lamp in enumerate(lamps):
			(x,y,z) = pixelSet[i]
			rgb(lamp, x, y, z, transitiontime = 3)
		sleep(period)
