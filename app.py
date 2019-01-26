from flask import Flask,redirect
from flask_basicauth import BasicAuth
import subprocess, config, os, requests



vars = config.config()
v0 = '-g ' + str(vars[0])
v1 = str(vars[1])
v2 = str(vars[2])
v3 = str(vars[3])
v4 = str(vars[4])
folder = os.path.dirname(os.path.realpath(__file__))
ap = Flask(__name__,static_url_path="",static_folder=folder)

# ap.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(ap)

#print vars[0],vars[1],vars[2],vars[3]
@ap.route('/')
def hello():
	return ap.send_static_file('main.html')

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

