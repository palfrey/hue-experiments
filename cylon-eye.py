from hue import *
from time import sleep

def cylon(i):
	for lamp in range(1,4):
		diff = abs(lamp-i)
		value = 255 - (diff*255)
		print lamp, i, diff, value
		rgb(lamp, value, 0, 0)
	sleep(.2)

while True:
	diff = .2
	for i in frange(1.0, 3.0, diff):
		cylon(i)
	for i in frange(3.0, 1, -diff):
		cylon(i)
