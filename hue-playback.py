from hue import *
import pickle
from time import sleep
from sys import argv
from audio_frames import play_audio

pixels = pickle.load(open(argv[1] + ".pixels"))
period = float(argv[2])

lamps = [int(x) for x in argv[3:]]

if len(lamps) == 0:
	raise Exception, "need some lamps"

play_audio(argv[1])

while True:
	for pixelSet in pixels:
		for i, lamp in enumerate(lamps):
			(x,y,z) = pixelSet[i]
			rgb(lamp, x, y, z, transitiontime = 3)
		sleep(period)
