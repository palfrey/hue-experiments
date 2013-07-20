from hue import *
from sys import argv

one, two, three = [int(x) for x in argv[1:]]
rgb(3, one, two, three, transitiontime = 1)
