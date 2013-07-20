import requests
import json
from colorpy import colormodels

ip = "169.254.87.149"
key = "7278ce1e7d0c44811ab4f854b75a234e"
base = "http://" + ip + "/api/" + key

def lights():
	data = requests.get(base).json
	lights = sorted(data["lights"].keys())
	return lights

def frange(start, stop, step):
    while start < stop:
        yield start
        start += step

def set_state(light, state):
	path = base + "/lights/%s/state" % light
	data = json.dumps(state)
	resp = requests.request("PUT", path, data=data)
	print resp.json

def rgb(light, red, green=None, blue=None, transitiontime=1):
	if isinstance(red, basestring):
		# assume a hex string is passed
		rstring = red
		red = int(rstring[1:3], 16)
		green = int(rstring[3:5], 16)
		blue = int(rstring[5:], 16)

	# We need to convert the RGB value to Yxy.
	redScale = float(red) / 255.0
	greenScale = float(green) / 255.0
	blueScale = float(blue) / 255.0
	colormodels.init(
		phosphor_red=colormodels.xyz_color(0.64843, 0.33086),
		phosphor_green=colormodels.xyz_color(0.4091, 0.518),
		phosphor_blue=colormodels.xyz_color(0.167, 0.04))
	xyz = colormodels.irgb_color(red, green, blue)
	xyz = colormodels.xyz_from_rgb(xyz)
	xyz = colormodels.xyz_normalize(xyz)

	return set_state(light, {"xy": [xyz[0], xyz[1]], "transitiontime": transitiontime, "on": True})
