from flask import Flask,redirect
import subprocess

app = Flask(__name__,static_url_path="",static_folder='/home/pi/Webserver/')
@app.route("/")

def hello():
	return app.send_static_file('index.html')

@app.route('/on')
def l_on():
	subprocess.call(['/usr/local/bin/rpi-rf_send','-g21','1655303'])
	return redirect('/')

@app.route('/off')
def l_off():
	subprocess.call(['/usr/local/bin/rpi-rf_send','-g21','1655302'])
	return redirect('/')

@app.route('/on1')
def l_on1():
	subprocess.call(['/usr/local/bin/rpi-rf_send','-g21','6832647'])
	return redirect('/')

@app.route('/off1')
def l_off1():
	subprocess.call(['/usr/local/bin/rpi-rf_send','-g21','6832646'])
	return redirect('/')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port = 80)

