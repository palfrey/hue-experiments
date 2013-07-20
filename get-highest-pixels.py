from video_frames import *
from sys import argv
import pickle

values = []

def looping_msg(msg):
	if msg.type == gst.MESSAGE_EOS:
		duration = pipeline.query_duration(gst.FORMAT_TIME)
		print 'Duration', duration

def new_storage(image, pipeline):
	global values
	colours = image.getcolors(image.size[0] * image.size[1])
	biggest = sorted(colours, key = lambda x: sum(x[1]))[-1]
	values.append(biggest)
	print biggest
	values.append(biggest)

run_pipeline(sys.argv[1], pixel_func = new_storage)
pickle.dump(values, open(sys.argv[1] + ".highest", "w"))

