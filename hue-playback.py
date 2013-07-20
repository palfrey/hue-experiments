from hue import *
import pickle
from time import sleep
from sys import argv

pixels = pickle.load(open(argv[1]))

while True:
	for (x,y,z) in pixels:
		rgbHsv(3, x, y, z, transitiontime = 3)
		sleep(0.15)
