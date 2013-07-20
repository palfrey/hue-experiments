import pickle
import numpy

tf = "times.pickle"
times = pickle.load(open(tf))

for key in sorted(times.keys()):
	data = numpy.array(sorted(times[key]))
	print key, numpy.mean(data), numpy.std(data)
