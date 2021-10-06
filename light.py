import datetime, pytz,time,json,requests,os,sys
from suntime import Sun, SunTimeException
lat = 37.69
lon = -113.07

def sendRequest(): # send a request to my server to turn the light on
    try:
        payload = {
            "arg":"on",
            "user":sys.argv[1],# saved as args because I don't want to add a file to github with my login stuff, and my server isn't configured to use a token or anything :(
            "password":sys.argv[2],
        }
        r = requests.get("https://ejsmith.hopto.org/control/go", params=payload)
        return True
    except:
        print("Unable to contact server, continuing")
        return False
def getSunsetTime(when=None):
    s = Sun(lat,lon)
    if not when:
        when = datetime.datetime.now()
    sunsetToday = s.get_sunset_time(when)
    r = sunsetToday + datetime.timedelta(days=1) # library has off by 1 day, unsure why ? ( known issue? )
    print(f"Next sunset at: {r.strftime('%m/%d/%y %H:%M')}")
    return r

try: # check if the arguments are set
    a = sys.argv[1]
except:
    print("Please provide a user [1] and password [2] to authticate to the webserver as the program args  :) ")
    quit()
while True:
    now = pytz.UTC.localize(datetime.datetime.utcnow())
        #now = now.replace(tzinfo=None)
    if 'sunsetToday' not in locals(): # if it's a new day, check when the new sunset is
        sunsetToday = getSunsetTime()
    elapsed = sunsetToday- now # gives the amount of time between now and the sunset
    #print(f"elasped:: {elapsed}")
    if elapsed.total_seconds() <= 40 :# if our time is within about a minute of the sunset time, turn on the light
        print("SUNSET! activating...")
        sendRequest()
        # set the next sunset to tomorrow?
        sunsetToday = getSunsetTime(datetime.datetime.now() + datetime.timedelta(days=1))
    print("")
    print(f"Time: {now.strftime('%m/%d %H:%M')}     Sunset: {sunsetToday.strftime('%m/%d %H:%M')}") # additional logging for debug sake ?
    print(f"remaining seconds until next sunset: {int(elapsed.total_seconds())}")
    time.sleep(60)# run only once per minute
