import datetime, pytz,time,json,requests,os,sys
from suntime import Sun, SunTimeException
lat = 37.6963 # my exact address monkas
lon = -113.0707
margin = datetime.timedelta(seconds=90) # margin so that the light only turns on at the specific time, and not constantly after sunset

def sendRequest(): # send a request to my server to turn the light on
    payload = {
        "arg":"on",
        "user":sys.argv[1],
        "password":sys.argv[2],
    }
    r = requests.get("https://ejsmith.hopto.org/control/go", params=payload)
def getSunsetTime():
    s = Sun(lat,lon)
    sunsetToday = s.get_local_sunset_time()
    sunsetToday += datetime.timedelta(days=1) # for some reason the day is off by one... so add one
    print(f"Sunset Today at {sunsetToday.strftime('%H:%M')}")
    return sunsetToday
try:
    a = sys.argv[1]
    #b = sys.argv[2]
except:
    print("Please provide a user and password to authticate to the webserver as the program args  :) ")
    quit()
while True:
    now = pytz.UTC.localize(datetime.datetime.now())
    if 'sunsetToday' not in locals() or now.date() > sunsetToday.date():
        sunsetToday = getSunsetTime()
    if now-margin <=  sunsetToday <= now+margin:
        print("Turn on! ")
        sendRequest()
    else:
        print("Don't Turn on! ")
    time.sleep(60)# check once per minute if we are in the correct time range to turn on ...
