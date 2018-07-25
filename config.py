def config():
	# this is the variables that need to be set
	# This is the GPIO data pin that is connected to the RF sender module
	rpi_gpio_pin = 21
	# These are the codes sent by the RPI to toggle lights
	outlet1on = 1655303
	outlet1off = 1655302
	# there should be 2 codes per light, one for on, and one for off ( if it works like mine does )
	outlet2on = 6832647
	outlet2off = 6832646
	# The path to where your webserver is being sent from. this is generally the location that this file currently is
	path_to_webserver = '/home/pi/rpi_lightserver/'
	return rpi_gpio_pin,outlet1on,outlet1off,outlet2on,outlet2off,path_to_webserver
