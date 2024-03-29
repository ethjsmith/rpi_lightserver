import datetime, pytz,time,json,requests,os,sys
from suntime import Sun, SunTimeException
import subprocess
lat = 37.69
lon = -113.07

def sendRequest():
    rpi_gpio_pin = '-g 21'
    outlet1on = '1655303'
    subprocess.call(['/usr/local/bin/rpi-rf_send',rpi_gpio_pin,outlet1on])


def sendWebRequest(): # send a request to my server to turn the light on, works best if the script is not running on the local network. 
# man I love not having a line limit LOL 
    try:
        payload = {
            'arg':'on',
            'user':sys.argv[1],# saved as args because I don't want to add a file to github with my login stuff, and my server isn't configured to use a token or anything :(
            'password':sys.argv[2],
        }
        r = requests.get('https://ejsmith.hopto.org/control/go', params=payload)
        return True
    except:
        print('Unable to contact server, continuing')
        return False
def getSunsetTime(when=None):
    s = Sun(lat,lon)
    if when is None:
        when = datetime.datetime.now()
    sunsetToday = s.get_sunset_time(when)
    sunsetToday = sunsetToday + datetime.timedelta(days=1)# library has off by 1 day, unsure why ? ( known issue? )
    print(f'Next sunset at: {sunsetToday.strftime("%m/%d/%y %H:%M")}')
    return sunsetToday
def iterate(now): # a test function for making time move a little faster than real-time
    now += datetime.timedelta(hours=10)
    print(f' now: {now.strftime("%m/%d %H:%M")}')
    return now
try: # check if the arguments are set
    a = sys.argv[1]
except:
    print('Please provide a user [1] and password [2] to authticate to the webserver as the program args  :) ')
    quit()
while True:
    now = pytz.UTC.localize(datetime.datetime.utcnow())
    if 'sunsetToday' not in locals(): # if it's a new day, check when the new sunset is
        sunsetToday = getSunsetTime()
    elapsed = sunsetToday- now # gives the amount of time between now and the sunset
    #print(f'elasped:: {elapsed}')
    if elapsed.total_seconds() <= 40 :# if our time is within about a minute of the sunset time, turn on the light
        print('SUNSET! activating...')
        print('')
        print(f'Time: {now.strftime("%m/%d %H:%M")}     Sunset: {sunsetToday.strftime("%m/%d %H:%M")}') # additional logging for debug sake ?
        print(f'remaining seconds until next sunset: {int(elapsed.total_seconds())}')
        sendRequest()
        # set the next sunset to tomorrow?
        sunsetToday = getSunsetTime(now) # testing this removed ?
    time.sleep(60)# run only once per minute
