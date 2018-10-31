#!/bin/bash

uwsgi --socket 0.0.0.0:80 --chdir /home/pi/rpi_lightserver/ --protocol=http -w wsgi:app
