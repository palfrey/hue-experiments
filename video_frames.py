import os
import sys
import gst
from os.path import exists
import pickle

from PIL import Image
from StringIO import StringIO

pixels = []

def append_struct(name, value, aggregate):
	aggregate[name] = value
	return True

def pixel_storage(image, pipeline):
	global pixels
	pixels.append(get_pixels(image))
	print len(pixels)
	if len(pixels)>200:
		return False

def get_pixels(img, pipeline):
	(w, h) = img.size
	locs = [(w/3.0, h/3.0), (w*(2/3.0), h/3.0), (w*(2/3.0), h*(2/3.0)), (w/3.0, h*(2/3.0))]
	locs = [(int(a), int(b)) for (a,b) in locs]
	return [img.getpixel(loc) for loc in locs]

def new_buffer(appsink, pixel_func = pixel_storage):
	buf = appsink.emit('pull-buffer')#,gst.Caps("image/png"))
	caps = buf.get_caps()
	items = {}
	for i in range(caps.get_size()):
		struct = caps.get_structure(i)
		for x in range(struct.n_fields()):
			struct.foreach(append_struct, items)
	img = Image.fromstring("RGB",(items["width"], items["height"]), str(buf))
	ret = pixel_func(img, pipeline)
	if ret == False:
		pipeline.set_state(gst.STATE_PAUSED)

def build_pipeline(path, caps=gst.Caps("video/x-raw-rgb"), pixel_func = pixel_storage):
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
	appsink.connect('new-buffer', new_buffer, pixel_func)
	pipeline.props.video_sink = appsink
	return pipeline

def on_msg(msg):
	if msg.type == gst.MESSAGE_ERROR:
		error, debug = msg.parse_error()
		print error, debug
	elif msg.type == gst.MESSAGE_EOS:
		duration = pipeline.query_duration(gst.FORMAT_TIME)
		print 'Duration', duration
		return False
	elif msg.type == gst.MESSAGE_STATE_CHANGED:
		(old, new, pending) = msg.parse_state_changed()
		if old == gst.STATE_PLAYING and new == gst.STATE_PAUSED:
			return False
	
	return True

pipeline = None

def run_pipeline(video_file, pixel_func = pixel_storage):
	global pipeline
	pipeline = build_pipeline(video_file, pixel_func = pixel_func)
	bus = pipeline.get_bus()
	pipeline.set_state(gst.STATE_PLAYING)
	pipeline.get_state()
	while True:
		msg = bus.poll(gst.MESSAGE_ANY, -1)
		ret = on_msg(msg)
		if ret == False:
			break

def main():
	global pixels
	pixel_file = sys.argv[1] + ".pixels"
	if not exists(pixel_file):
		run_pipeline(sys.argv[1])
		print pixels
		pickle.dump(pixels, open(pixel_file, "w"))

if __name__ == '__main__':
	main()
