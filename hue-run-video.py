from video_frames import *
from hue import *
from sys import argv
from time import sleep

lamps = [int(x) for x in argv[2:]]

if len(lamps) == 0:
	raise Exception, "need some lamps"

def new_storage(image, pipeline):
	currentPixels = get_pixels(image)
	for i, lamp in enumerate(lamps):
		(x,y,z) = currentPixels[i]
		rgb(lamp, x, y, z, transitiontime = 1)
	move_forward(pipeline, 0.3)
	sleep(0.3)

def move_forward(pipeline, amount):
	pos_int = pipeline.query_position(gst.FORMAT_TIME, None)[0]
	seek_ns = pos_int + (amount * 1000000000)
	pipeline.seek_simple(gst.FORMAT_TIME, gst.SEEK_FLAG_FLUSH, seek_ns)

run_pipeline(sys.argv[1], pixel_func = new_storage)

