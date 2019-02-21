from flask import Flask,redirect
from flask_basicauth import BasicAuth
from resources import templates, content
import subprocess, config, os, requests, secret


vars = config.config()
v0 = '-g ' + str(vars[0])
v1 = str(vars[1])
v2 = str(vars[2])
v3 = str(vars[3])
v4 = str(vars[4])
folder = os.path.dirname(os.path.realpath(__file__))
ap = Flask(__name__,static_url_path="",static_folder=folder)

# creates the template object
templ = templates.Template()

#also creates the cotent object
cont = content.Content()


# you'll need to create a secret.py file which returns (username,password)
# check the readme for more information about how to do this, with an example
creds = secret.creds()
ap.config['BASIC_AUTH_USERNAME'] = creds[0]
ap.config['BASIC_AUTH_PASSWORD'] = creds[1]

# ap.config['BASIC_AUTH_FORCE'] = True
# this is basically a way better version of a php template, throw this onto any funtion's return to make 
# that page have a top nav bar... saves a lot of effort! 
header = templ.header() 
#stylesheet = """<link rel = "stylesheet" href = "style.css">"""
stylesheet = templ.stylesheet()
basic_auth = BasicAuth(ap)

#print vars[0],vars[1],vars[2],vars[3]
@ap.route('/')
def hello():
	#return ap.send_static_file('main.html')
	return ' <html><head>' + stylesheet +"""<title>Home</title></head>
<body> """ + header + """ <h1> Homepage </h1>
<p class = "card"> Welcome to my cool site... coolness coming soon</p>
</body>
</html>"""

@ap.route('/projects')
def projects():
	return """<html>
	<head>
		<link rel="stylesheet" href="style.css">
		<title> Projects </title>
	</head>
	<body>
	""" + header + """ <h1> Projects </h1><div class = "card">Welcome to the projects page. this site is actually my main project right now
	This page is the first one being served directly from the flask app, instead of from a static html file...
	I think that's pretty cool, and it also allows me to do stuff like the header, without using php... nice</div>
	</body>
</html>
"""
@ap.route('/misc')
def misc():
	return '<html>' + stylesheet + header + '''<h1> Random Stuff </h1> <div class ="card">
Probably I will just post about video games here or something... 
<br><a href = "/misc/aoe">Age of Empires 2</a>
<br><a href = "/misc/dishonored"> Dishonored</a></div>
</html>'''
# ap route for all the games under misc in route ? hopefully anyway! 
@ap.route('/misc/<path:router>')
def misc_route(router):
#	if getattr(templ,path,"nope") != "nope" and getattr(templ,path,"nope") != page and getattr(templ,path,"nope") != header and getattr(templ,path,"nope") != stylesheet:
#		return templ.page(path,templ.templ.getattr(templ,path))
#	else:
#		return "No page found"
	if getattr(cont,str(router),"error") != "error":
		runme = getattr(cont,str(router),"error")
		return templ.page(str(router),runme())
	else:
		return templ.page("error",templ.error())
#@ap.route('/misc/aoe')
#def misc_aoe():
#	return templ.page("aoe",templ.aoe())
@ap.route('/about')
def about():
	return '<html>' + stylesheet + header + '''<h1> About Me</h1> <div class = "card">
My name is Ethan Smith, and I am a CSIS student at Southern Utah University.
at SUU I am also the Vice President of the cyber defence (&competition ) club, and a
student security analyst.</div>
</html>'''

@ap.route('/control')
@basic_auth.required
def controller():
	return ap.send_static_file('index.html')

@ap.route('/control/on')
@basic_auth.required
def l_on():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v1])
	return redirect('/control')

@ap.route('/control/off')
@basic_auth.required
def l_off():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v2])
	return redirect('/control')

@ap.route('/control/on1')
@basic_auth.required
def l_on1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v3])
	return redirect('/control')

@ap.route('/control/off1')
@basic_auth.required
def l_off1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v4])
	return redirect('/control')

@ap.route('/control/heatoff')
@basic_auth.required
def h_off():
	r = requests.get('http://192.168.0.16/off')
	return redirect('/control')

@ap.route('/control/heatlow')
@basic_auth.required
def h_low():
	r = requests.get('http://192.168.0.16/low')
	return redirect('/control')

@ap.route('/control/heatmid')
@basic_auth.required
def h_mid():
	r = requests.get('http://192.168.0.16/mid')
	return redirect('/control')

@ap.route('/control/heathigh')
@basic_auth.required
def h_high():
	r = requests.get('http://192.168.0.16/high')
	return redirect('/control')

if __name__ == "__main__":
	ap.run(debug=True, host='0.0.0.0')

