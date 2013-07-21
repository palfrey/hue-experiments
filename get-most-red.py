from video_frames import *
from sys import argv
import pickle

values = []

def new_storage(image, pipeline):
	global values
	locations = [(429, 243), (633, 231), (859, 240)]
	pixels = [image.getpixel((x,y))[::-1] for (x,y) in locations]
	values.append(pixels)
	print len(values)
	#if len(pixels) > 200:
	#	return False

run_pipeline(sys.argv[1], pixel_func = new_storage)
pickle.dump(values, open(sys.argv[1] + ".pixels", "w"))

