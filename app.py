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
app = Flask(__name__,static_url_path="",static_folder=folder)

app.config['BASIC_AUTH_USERNAME'] = 'ejsmith_user'
app.config['BASIC_AUTH_PASSWORD'] = '@allianceWithTheBlackHole11'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

#print vars[0],vars[1],vars[2],vars[3]
@app.route('/')
def hello():
	return app.send_static_file('index.html')
@app.route('/on')
def l_on():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v1])
	return redirect('/')

@app.route('/off')
def l_off():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v2])
	return redirect('/')

@app.route('/on1')
def l_on1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v3])
	return redirect('/')

@app.route('/off1')
def l_off1():
	subprocess.call(['/usr/local/bin/rpi-rf_send',v0,v4])
	return redirect('/')

@app.route('/heatoff')
def h_off():
	r = requests.get('http://192.168.0.16/off')
	return redirect('/')

@app.route('/heatlow')
def h_low():
	r = requests.get('http://192.168.0.16/low')
	return redirect('/')

@app.route('/heatmid')
def h_mid():
	r = requests.get('http://192.168.0.16/mid')
	return redirect('/')

@app.route('/heathigh')
def h_high():
	r = requests.get('http://192.168.0.16/high')
	return redirect('/')

if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0', port = 80)

