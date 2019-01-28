#!/bin/bash

# install dependancies
sudo apt update
sudo apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv nginx
### check for ufw, and if it exists open the ports for nginx
### sudo ufw allow 'Nginx Full'

mkdir ~/$1
cd ~/$1
python3 -m venv $1
source $1/bin/activate
sudo pip install wheel rpi-rf Flask Flask-BasicAuth uwsgi
deactivate

### make a copy of the config file so that it can be copied onto different systems
sudo cp $todo_here /etc/systemd/system/app.service
sudo systemctl enable app
sudo systemctl start app

### set up nginx 
