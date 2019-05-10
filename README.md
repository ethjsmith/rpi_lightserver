# rpi_lightserver
the simple web server that runs on my raspberry pi, which controls all of my homemade IOT devices, and also serves dynamic python-generated webpages... Don't tell me about best practice, I don't belive in it.



# Update 

Almost all of the readme is now obsolete, as the scope of the project has changed pretty drastically
there are still some partially working scripts in the "scripts" folder, if you are really trying to set this up yourself.

TODO: redo todo
TODO: rewrite this README from the ground up
TODO: change how page content is imported

# TODO : 
~~~add enviroment variables for username and password ( for sites basic auth ( for now those lines are just cut out of the program ) )~~~
~~~clean up config file (config.py ) ~~~
~~~improve the website section of the project ( make it a real site, not just 2 lines of placeholder text )~~~
~~~add functionallity to the website ( like php for consistent topbars, and site navigation ) ~~~
clean up the readme beyond this point
learn more about web standards, and how higher level parts of the project like nginx work

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

** uWSGI **

uWSGI is used as a better webserver. flask's internal server is really only meant for testing, while this one is better for a production environment, like 
the site that is open to the world...
` pip install uwsgi `

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

TODO
