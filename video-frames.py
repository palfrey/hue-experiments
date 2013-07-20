import os
import sys
import gst
from os.path import exists
import pickle

from PIL import Image
from StringIO import StringIO

def get_frame(path, caps=gst.Caps("video/x-raw-rgb")):
	uri = 'file://' + os.path.abspath(path)
	#pipe = "uridecodebin uri=%s ! ffmpegcolorspace ! videoscale ! appsink name=proc_sink caps=\"%s\"" % ('file://' + os.path.abspath(path), "image/png")
	pipe = "playbin2 uri=%s"% uri
	print pipe
	pipeline = gst.parse_launch(pipe)

	#appsink = list(pipeline.elements())[0]
	pipeline.props.audio_sink = gst.element_factory_make("fakesink")
	appsink = gst.element_factory_make("appsink")
	appsink.props.caps = caps
	appsink.props.max_buffers = 1
	appsink.props.emit_signals = True
	appsink.connect('new-buffer', new_buffer)
	pipeline.props.video_sink = appsink
	return pipeline

pixels = []

def append_struct(name, value, aggregate):
	aggregate[name] = value
	return True

def new_buffer(appsink):
	global pixels
	buf = appsink.emit('pull-buffer')#,gst.Caps("image/png"))
	caps = buf.get_caps()
	items = {}
	for i in range(caps.get_size()):
		struct = caps.get_structure(i)
		for x in range(struct.n_fields()):
			struct.foreach(append_struct, items)
	img = Image.fromstring("RGB",(items["width"], items["height"]) , str(buf))
	(w, h) = img.size
	locs = [(w/3.0, h/3.0), (w*(2/3.0), h/3.0), (w*(2/3.0), h*(2/3.0)), (w/3.0, h*(2/3.0))]
	locs = [(int(a), int(b)) for (a,b) in locs]
	currentPixels = [img.getpixel(loc) for loc in locs]
	pixels.append(currentPixels)
	print len(pixels)
	if len(pixels)>200:
		pipeline.set_state(gst.STATE_PAUSED)

def on_msg(msg):
	if msg.type == gst.MESSAGE_ERROR:
		error, debug = msg.parse_error()
		print error, debug
	elif msg.type == gst.MESSAGE_EOS:
		duration = pipeline.query_duration(gst.FORMAT_TIME)
		print 'Duration', duration
	elif msg.type == gst.MESSAGE_STATE_CHANGED:
		(old, new, pending) = msg.parse_state_changed()
		if old == gst.STATE_PLAYING and new == gst.STATE_PAUSED:
			return False
	
	return True

pipeline = None

def main():
	pixel_file = sys.argv[1] + ".pixels"
	if not exists(pixel_file):
		global pipeline, pixels
		pipeline = get_frame(sys.argv[1])

		print list(pipeline.elements())

		bus = pipeline.get_bus()
		pipeline.set_state(gst.STATE_PLAYING)
		pipeline.get_state()
		while True:
			msg = bus.poll(gst.MESSAGE_ANY, -1)
			ret = on_msg(msg)
			if ret == False:
				break

		print pixels
		pickle.dump(pixels, open(pixel_file, "w"))

if __name__ == '__main__':
	main()
