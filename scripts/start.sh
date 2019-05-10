#!/bin/bash

# this line is only if you are testing, or running only the wsgi portion of the server, which isn't reccomended
uwsgi --socket 0.0.0.0:80 --chdir /home/pi/rpi_lightserver/ --protocol=http -w wsgi:app
