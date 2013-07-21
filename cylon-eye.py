from hue import *
from time import sleep

def cylon(light, start = 0):
	while True:
		for i in range (start, 255, 20):
			rgb(light, i, 0, 0)
			yield None
		for i in range (255, 0, -20):
			rgb(light, i, 0, 0)
			yield None

cylons = [
		cylon(3),
		cylon(2, 128),
		cylon(1, 255)
		]

while True:
	for c in cylons:
		c.next()
	sleep(.2)
