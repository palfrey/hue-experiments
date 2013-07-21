from hue import *
import pickle
from time import sleep, time
from sys import argv
from audio_frames import play_audio

pixels = pickle.load(open(argv[1]))
period = .2

lamps = [int(x) for x in argv[2:]]

if len(lamps) == 0:
	raise Exception, "need some lamps"

for other in [x for x in lights() if x not in lamps]:
	off(other)

highest = max(x[0] for x in pixels)
print highest

start = time()
done_thunder = False

while True:
	last_bri = None
	for (count, (r,g,b)) in pixels:
		bri = (count*1.0)/highest

		mod_bri = int(bri * 10)
		if mod_bri > 0 and bri != last_bri:
			print "bri", bri, count, highest
			for lamp in lamps:
				hsv(lamp, 0, 0, bri, transitiontime = 1)
			sleep(period)
			last_bri = bri
			if time()-start > 3.0:
				play_audio("thunder.wav")
				start += 8.0
