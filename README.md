# rpi_lightserver
the simple web server that runs on my raspberry pi, which controls my lights
Now you can set it up yourself as well!, just follow the poorly written instructions below


# Hardware Requirements

**A raspberry PI**

pi3 perferred but should work with pi2 as well 

**RF transmitter and reciver** 

here is the stuff that I am using in this project. you do need the receiver in order to find your outlet's frequency

https://www.amazon.com/gp/product/B017AYH5G0/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1
 
**wireless outlet**

These are the outlets I am using, although this project should work for any 433mhz outlet

https://www.amazon.com/gp/product/B01FHIG5GW/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1

you will need to find the RF frequency of your outlets. to do this, I used an
RF_sniffer program, and the remote that came with my outlet. this program is 
currently hard coded to work with my set only, Ill fix that in a future update

# Installing

**RPI-rf**

https://github.com/milaq/rpi-rf

This is the program I use to send rf signals. it really simplifys the process, and it works great.
install it with : 
```
sudo apt-get install python3-pip
sudo pip3 install rpi-rf
```

**Flask**

I use flask to host the webserver that I am running, because it is simple and works well for this small scale project
install it  with : ( now also install basicauth, which allows you to log into the webserver, making it safer to be exposed to the outside world ) install with : 
```
pip install Flask
pip install Flask-BasicAuth
```
**RFSniffer**

I use this program to find the frequency that your wifi remote is set to. With some outlets you can find out directly from
the manufacterer, or even on the product it'sself, but for me, I used this program
```
TODO Write/finish a better tutorial for this part
```

**finishing up**

Once you have all of this set up, you should be good to go, just run the program with 
```
sudo python app.py
```

**startup**

One final thing to try is setting the program to run whenever the RPI restarts, so that it is always running ( barring a crash or internet outage)
you can do this by editing your /etc/rc.local file with this line
```
 TODO add the line here
```
