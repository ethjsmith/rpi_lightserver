# rpi_lightserver
the simple web server that runs on my raspberry pi, which controls my lights


# Requirements : 

A raspberry PI (v3 perferred but should work with v2 as well ) 

jumper cables connecting the RF sender module to the (currently) hard wired pins


you need a RF sender , as well as something to recive the signal,
here is the stuff that I am using in this project
https://www.amazon.com/gp/product/B017AYH5G0/ref=oh_aui_detailpage_o08_s00?ie=UTF8&psc=1
and 
https://www.amazon.com/gp/product/B01FHIG5GW/ref=oh_aui_detailpage_o01_s00?ie=UTF8&psc=1

you will need to find the RF frequency of your outlets. to do this, I used an
RF_sniffer program, and the remote that came with my outlet. this program is 
currently hard coded to work with my set only, Ill fix that in a future update

https://github.com/milaq/rpi-rf
the webserver calls this program, so you also have to install it,
although it is pretty simple, just :
sudo apt-get install python3-pip
sudo pip3 install rpi-rf 

and you should be good to go !


