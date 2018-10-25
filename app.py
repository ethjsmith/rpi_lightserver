from flask import Flask,redirect
from flask_basicauth import BasicAuth
import subprocess, config, os

vars = config.config()
#app = Flask(__name__,static_url_path="",static_folder=vars[5])
app = Flask(__name__,static_url_path="",static_folder=os.path.dirname(os.path.realpath(__file__)))

app.config['BASIC_AUTH_USERNAME'] = 'ejsmith'
app.config['BASIC_AUTH_PASSWORD'] = 'password'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

@app.route("/")
@basic_auth.required
def hello():
	return app.send_static_file('index.html')

@app.route('/on')
@basic_auth.required

def l_on():
	subprocess.call(['/usr/local/bin/rpi-rf_send',vars[0],vars[1]])
	return redirect('/')

@app.route('/off')
@basic_auth.required
def l_off():
	subprocess.call(['/usr/local/bin/rpi-rf_send',vars[0],vars[2]])
	return redirect('/')

@app.route('/on1')
@basic_auth.required

def l_on1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',vars[0],vars[3]])
	return redirect('/')

@app.route('/off1')
@basic_auth.required
def l_off1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',vars[0],vars[4]])
	return redirect('/')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80)

