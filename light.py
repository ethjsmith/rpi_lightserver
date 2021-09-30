import datetime, pytz,time,json,requests,os,sys
from suntime import Sun, SunTimeException
lat = 37.69
lon = -113.07

def sendRequest(): # send a request to my server to turn the light on
    payload = {
        "arg":"on",
        "user":sys.argv[1],# saved as args because I don't want to add a file to github with my login stuff, and my server isn't configured to use a token or anything :(
        "password":sys.argv[2],
    }
    r = requests.get("https://ejsmith.hopto.org/control/go", params=payload)
def getSunsetTime():
    s = Sun(lat,lon)
    sunsetToday = s.get_local_sunset_time()
    sunsetToday += datetime.timedelta(days=1) # for some reason the day is off by one... so add one
    print(f"Sunset: {sunsetToday.strftime('%d/%m/%y %H:%M')}")
    return sunsetToday


try: # check if the arguments are set
    a = sys.argv[1]
except:
    print("Please provide a user [1] and password [2] to authticate to the webserver as the program args  :) ")
    quit()
while True:
    now = pytz.UTC.localize(datetime.datetime.now())
    if 'sunsetToday' not in locals() or now.date() > sunsetToday.date(): # if it's a new day, check when the new sunset is
        sunsetToday = getSunsetTime()
    elapsed = now - sunsetToday
    if -40 <= elapsed.total_seconds() <= 40 :# if our time is within about a minute of the sunset time, turn on the light
        print("Turn on! ")
        sendRequest()
    else:
        print("Don't Turn on! ")
    print(f"Time: {now.strftime('%d/%m/%y %H:%M')} and Sunset Time: {sunsetToday.strftime('%d/%m/%y %H:%M')}") # additional logging for debug sake ?
    print(f"delta: {elapsed} and remaining seconds: {elapsed.total_seconds()}")
    time.sleep(60)# run only once per minute
