# rpi_lightserver
the simple web server that runs on my raspberry pi, which controls all of my homemade IOT devices, and also serves dynamic python-generated webpages... Don't tell me about best practice, I don't belive in it.

# credentials :
for this project you need a file called "secret.py" in the same directory as the app.py, where you save the credentials.
this can be a very simple file, that looks something like this.
```
def creds():
	user = "username_here"
	passw = "password_here"
	return user,passw
```
this will allow pages with basicauth to have credentials that aren't shared in the github ( as my .gitignore ignores the file "secret.py" )

# Hardware Requirements

..* [A raspberry pi](https://www.raspberrypi.org/) is required for all of the features in the control and video sections to work, I would suggest a PI4, as it is the newest, and most powerful, but hypothetically any device would work.(certainly pi3 does)

..* [GPIO Transmitters and receivers](https://www.amazon.com/gp/product/B017AYH5G0/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1) are the transmitters that I am using in this project. you do need the receiver in order to find your outlet's frequency, unless it is included in the documentation for your outlet


..* [433mhz Wireless outlets to recive radio signals](https://www.amazon.com/gp/product/B01FHIG5GW/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1) are the outlets I am using, although this project should work for any 433mhz compatible outlet

..* [a raspberry pi camera ](https://www.raspberrypi.org/products/camera-module-v2/) for a view-able live stream

you will need to find the RF frequency of your outlets. to do this, I used an
RF_sniffer program, and the remote that came with my outlet. this program is
currently hard coded to work with my set only, Ill fix that in a future update

# Installing

**Python Package dependancies**


```
pip install Flask, flask_basicauth, flask_login, flask_sqlalchemy, uwsgi, rpi-rf
```
I use flask to host the webserver that I am running, because it is simple and works well for this small scale project
install it  with : ( now also install basicauth, which allows you to log into the webserver, making it safer to be exposed to the outside world

uWSGI is used as a better web server. flask's internal server is really only meant for testing, while this one is better for a production environment, like this site which is open to the world...

[rpi_rf](https://github.com/milaq/rpi-rf) is the program I use to send rf signals. it really simplifies the process, and it works great.



**RFSniffer**

I use this program to find the frequency that your wifi remote is set to. With some outlets you can find out directly from
the manufacterer, or even on the product it'sself, but for me, I used this program
```
TODO Write/finish a better tutorial for this part
```

**running a test version**

Once you have all of this set up, you should be good to go, just run the program with
```
sudo python3 app.py
```
which runs a test instance on port 5000 of your pc, allowing you to troubleshoot anything amiss with the python code ( like missing dependancies)

**service-ify**

if you've installed uwsgi, you can run the webserver as a service... the code for that would look something like this ( this is for default user pi on any raspberry pi)
```
[Unit]
Description=uWSGI serving python webserver
After=network.target

[Service]
User=pi
Group=www-data
WorkingDirectory=/home/pi/rpi_lightserver
Environment="PATH=/home/pi/rpi_lightserver/[YOUR VIRTUAL ENV NAME HERE!!!]/bin"
ExecStart=/home/pi/rpi_lightserver/[YOUR VIRTUAL ENV NAME HERE!!!]/bin/uwsgi --ini myproject.ini

[Install]
WantedBy=multi-user.target
```
just copy this code into /etc/systemd/system/app.service, and then run
```
sudo systemctl start app
sudo systemctl enable app
```
**nginx and more **

if you want the site to be accessible from outside, a good web request server like nginx would be a good addition. While not 100% required, it can be very helpful. 
