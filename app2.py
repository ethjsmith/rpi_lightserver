from flask import Flask,redirect,request
from flask_basicauth import BasicAuth
from resources import templates, miscContent, projectContent, blogContent
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
mcont = miscContent.Misc_Content()
pcont = projectContent.ProjectContent()
bcont = blogContent.blogContent()
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
	body = '<html>' + stylesheet + header + '''<h1> My Projects </h1> <div class ="card">
	Here is a list of some of the different projects I have worked on in the past. check out all the different things I'm interested in!</div><br>
	'''
	return body + templ.readContent(pcont,request.path) + "</html>"
@ap.route('/projects/<path:router>')
def projects_route(router):
	#router = '/projects/' + router
	return templ.generatePage(router,pcont)
# misc now dynamically reads in it's child articles, and creates a preview which links to each article.
@ap.route('/misc')
def misc():
	body =  '<html>' + stylesheet + header + '''<h1> Random Stuff </h1> <div class ="card">
The Misc page is home to anything that doesn't fit on any of the other pages. Reallistically I am probably just going to write about all my favorite video games here, but maybe
ill throw in some other stuff about things that are happening in my life. don't keep your fingers crossed for that.</div><br> '''
	body = body + templ.readContent(mcont,request.path) + "</html>"
	return body
# ap route for all the games under misc in route ? hopefully anyway! 
@ap.route('/misc/<path:router>')
def misc_route(router):
	#router = '/misc/' + router
#	if getattr(mcont,str(router),"error") != "error":
#		runme = getattr(mcont,str(router),"error")
#		return templ.page(str(router),runme())
#	else:
#		return templ.page("error",templ.error())
	return templ.generatePage(router,mcont)
@ap.route('/blog')
def blog():
	body = '<html>' + stylesheet + header + '''<h1> A blog? or something</h1><div class = "card">'''
	return body + templ.readContent(bcont,request.path) + "</html>"
@ap.route('blog/<path:router>')
def blog_route(router):
	return templ.generatePage(router,bcount)
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
	ap.run()

