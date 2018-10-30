#!/bin/bash

# install dependancies
sudo apt install python3-pip
sudo pip3 install rpi-rf Flask Flask-BasicAuth uwsgi

# activate the uwsgi as a service ( so that it is running in the background)

sudo systemctl start app
# set the service to autostart
sudo systemctl enable app
