import requests
import json
from colorpy import colormodels

ip = "172.16.20.39"
key = "7278ce1e7d0c44811ab4f854b75a234e"
base = "http://" + ip + "/api/" + key

def lights():
	data = requests.get(base).json
	lights = sorted(data["lights"].keys())
	return lights

def frange(start, stop, step):
	if step < 0:
		while start > stop:
			yield start
			start += step
	else:
		while start < stop:
			yield start
			start += step

def set_state(light, state):
	path = base + "/lights/%s/state" % light
	data = json.dumps(state)
	resp = requests.request("PUT", path, data=data)
	print resp.json

def rgbXY(light, red, green=None, blue=None, transitiontime=1):
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

	return set_state(light, {"xy": [xyz[0], xyz[1]], "transitiontime": transitiontime})#, "on": True})

def rgb_to_hsv_for_hue(r, g, b):
	maxc = max(r, g, b)
	minc = min(r, g, b)
	v = maxc
	if minc == maxc:
		return 0.0, 0.0, v
	s = (maxc-minc) / maxc
	rc = (maxc-r) / (maxc-minc)
	gc = (maxc-g) / (maxc-minc)
	bc = (maxc-b) / (maxc-minc)
	if r == maxc:
		h = bc-gc
	elif g == maxc:
		h = 2.0+rc-bc
	else:
		h = 4.0+gc-rc
	h = (h/6.0) % 1.0
	#magic numbers by hue bulb experimentation
	if h > .1 and h < .4: # make greens more green
		h += 0.06340123598 #(26000/65535)-(21845/65535)
	if h > .4 and h < .7: # make blues more blue
		h += 0.05050736247 #(47000/65535)-(43690/65535)
	return h, s, v

def rgb(light, red, green=None, blue=None, transitiontime=1):
	red = red/255.0
	green = green/255.0
	blue = blue/255.0
	(h,s,v) = rgb_to_hsv_for_hue(red, green, blue)
	return hsv(light, h, s, v, transitiontime)

def hsv(light, h, s, v, transitiontime = 1):
	print h,s,v
	h = int(h*65535)
	s = int(s*254)
	if v <=1.0:
		v = int(v*254)
	print h,s,v
	return set_state(light, {"hue": h, "sat": s, "bri": v, "transitiontime": transitiontime, "on": True})

def off(light):
	return set_state(light, {"on": False})
