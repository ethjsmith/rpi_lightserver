from flask import Flask,redirect,request
from flask_basicauth import BasicAuth
from werkzeug import secure_filename
from resources import templates, miscContent, projectContent, blogContent
import subprocess, config, os, requests, secret,sys


conf = config.config()
conf[0] = '-g ' + conf[0]
print (sys.version)
folder = os.path.dirname(os.path.realpath(__file__))
ap = Flask(__name__,static_url_path="",static_folder=folder)

# creates the template object
templ = templates.Template()

#also creates the cotent objects
mcont = miscContent.Misc_Content()
pcont = projectContent.ProjectContent()
bcont = blogContent.blogContent()
# you'll need to create a secret.py file which returns (username,password)
# check the readme for more information about how to do this, with an example
creds = secret.creds()
ap.config['BASIC_AUTH_USERNAME'] = creds[0]
ap.config['BASIC_AUTH_PASSWORD'] = creds[1]

# this is basically a way better version of a php template, throw this onto any funtion's return to make
# that page have a top nav bar... saves a lot of effort!
header = templ.header(0)
stylesheet = templ.stylesheet()
basic_auth = BasicAuth(ap)


@ap.route('/')
def homepage():
	return ' <html><head>' + stylesheet +"""<title>Home</title></head>
<body> """ + templ.header('/') + """ <h1> Homepage </h1><div class = "card">
<p> What do you even put on a homepage of a website that you built for fun?</p>
<p> Either way, welcome to ejsmithy.xyz, the website I built from the ground up using Python(flask) to avoid learning php for headers...</p>
<p> Check out the source code <a href = \"https://github.com/urd000med/rpi_lightserver\">Here </a> and see if you can find all the interesting secrets and unlisted pages...</p>
<p> Don't try to hack the site</p></div>
</body>
</html>"""

@ap.route('/projects')
def projects():
	body = '<html>' + stylesheet + templ.header('/projects') + '''<h1> My Projects </h1> <div class ="card">
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
	body =  '<html>' + stylesheet + templ.header('/misc') + '''<h1> Random Stuff </h1> <div class ="card">
The Misc page is home to anything that doesn't fit on any of the other pages. Realistically I am probably just going to write about video games here. </div><br> '''
	body = body + templ.readContent(mcont,request.path) + "</html>"
	return body
# ap route for all the games under misc in route ? hopefully anyway!
@ap.route('/misc/<path:router>')
def misc_route(router):
	return templ.generatePage(router,mcont)
@ap.route('/blog')
def blog():
	body = '<html>' + stylesheet + templ.header('/blog') + '''<h1> A blog? or something</h1><div class = "card">
	My life story up to this point... or at least some interesting stuff that I might write about from time to time</div><br>'''
	return body + templ.readContent(bcont,request.path) + "</html>"
@ap.route('/blog/<path:router>')
def blog_route(router):
	return templ.generatePage(router,bcont)
@ap.route('/secret')
def secret():
	return '<html>' + stylesheet + templ.header(0) + '''<h1> Secret page</h1> <div class = "card">
You found the secret page, good job!

Kind of anticlimactic to be honest</div></html>'''
@ap.route('/about')
def about():
	return '<html>' + stylesheet + templ.header('/about') + '''<h1> About Me</h1> <div class = "card">
<p>My name is Ethan Smith, and I am a CSIS student at Southern Utah University.
at SUU I am also the Vice President of the cyber defence (competition) club, and a
student security analyst. I love programming ( prefer Python and Java), Snowboarding during the winter, and playing lots of different video games. I also enjoy homemade IOT devices, and <br> Contact me at `ethan@esmithy.net` </p>
<p> About the site: <br> This site was built as a project, just something that I like to play around with when I have some downtime between work and school.
I had the idea to make a website which instead of having static html files and PHP templates, would use python to generate all the pages by chaining together string variables containing bits of html, which altogether would generate web pages. I've done a lot of things to try and make the site
scalable, instead of static, and I've really enjoyed putting it together, although writing html with python syntax highlighting can be a pain sometimes! </p>

</div>
</html>'''

# File sharing section
@ap.route('/files', methods = ['GET','POST'])
def files():
	if request.method == 'POST':
		f=request.files['file']
		f.save('./uploads/' + secure_filename(f.filename))
	links = ""
	uploadedfiles= os.listdir('uploads/')
	for z in uploadedfiles:
		links = links + "<a href = \"uploads/" + z + "\" >" + z + "</a><br>"
	return '<html>' + stylesheet + templ.header(0) + '<h1> File share </h1> <div class = \"card\"> <form method = \"POST\" enctype = \"multipart/form-data\"><input type = \"file\" name = \"file\" /><input type = \"submit\" value = \"upload file\"/></form></div><br><div class = \"card\">' + links + '</div></html>'
# delete a file in the list of file sharing section
# if you want to add a button to do this, that's pretty easy, there's an example of it
# in my test repo attached to the filesharing
@ap.route('/files/d/<path:filename>')
@basic_auth.required
def deletefile(filename):
	if os.path.exists('uploads/' + filename):
		os.remove('uploads/' + filename)
	return redirect('/files')

@ap.route('/control')
@basic_auth.required
def controller():
#	return ap.send_static_file('index.html')
	return '<html>' + stylesheet + templ.header('/control') + """<div class = \"card\"><p style=\"font-size:90px\"><a href=\"/control/go?arg=on\">Light On</a><br><a href=\"/control/go?arg=off\">Light Off</a><br><a href=\"/control/go?arg=on1\">Fan On(This doesnt do anything)</a><br><a href=\"/control/go?arg=off1\">Fan Off( This ones doesn\'t either lol)</a><br></p></div></html>"""
# outline of overhauled light controller
@ap.route('/control/go')
@basic_auth.required
def doEverything():
	if request.args.get('arg') != None:
		if request.args.get('arg') == "on":
			subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[1]])
		elif request.args.get('arg') == "off":
			subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[2]])
		elif request.args.get('arg') == "on1":
			subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[3]])
		elif request.args.get('arg') == "off1":
			subprocess.call(['/usr/local/bin/rpi-rf_send',conf[0],conf[4]])
		else:
			print ("error?")
	return redirect('/control')
#Heat system is currently legacy, everything used to work like this with it's own target, but now it's a bit cleaner ( or smaller at least)
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
