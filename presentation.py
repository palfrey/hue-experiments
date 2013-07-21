from os import system

while True:
	inp = raw_input("1) fire\n 2) lightning\n")
	try:
		option = int(inp)
		if option == 1:
			system("mplayer 'bring you fire.wav'")
			system("python hue-playback.py fire-B65crveP9WY.flv .2 3 1 2")
		elif option == 2:
			system("mplayer 'thunderbolts and lightning.wav'")
			system("python lightning.py lightning.mp4.highest 2")
		else:
			break
	except Exception, e:
		print e
		raise
