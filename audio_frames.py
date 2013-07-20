import os
import sys
import gst

def looping_msg(msg):
	if msg.type == gst.MESSAGE_EOS:
		duration = pipeline.query_duration(gst.FORMAT_TIME)
		print 'Duration', duration

def audio_only_pipeline(path):
	uri = 'file://' + os.path.abspath(path)
	pipe = "playbin2 uri=%s"% uri
	pipeline = gst.parse_launch(pipe)
	pipeline.props.video_sink = gst.element_factory_make("fakesink")
	return pipeline

def play_audio(path):
	pipeline = audio_only_pipeline(path)
	bus = pipeline.get_bus()
	bus.add_signal_watch
	pipeline.set_state(gst.STATE_PLAYING)
	pipeline.get_state()

def main():
	play_audio(sys.argv[1])
	from time import sleep
	while True:
		sleep(1.0)

if __name__ == '__main__':
	main()
