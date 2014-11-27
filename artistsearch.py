import urllib, urllib2, json

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def createURL(id, location, artist):
    base = 'http://api.bandsintown.com/events/search.json?artists[]=' + artist + '&location=' + location + '&app_id=' + id
    return base

def searchEvents(id, location, artist):
    try:
        readEvents = urllib2.urlopen(createURL(id, location,artist)).read()
    except Exception:
        print 'did not reach server'


    eventsData = json.loads(readEvents)
    if len(eventsData) == 0:
        print '%s is not coming to %s.' % (artist, location)
    else:
        date = eventsData[0]['datetime']
        print '%s will be in %s on %s.' % (artist, location, date)
   

try:
    urllib2.urlopen(createURL('dawgtunes', 'Seattle,WA', 'Bastille'))
except urllib2.URLError, e:
    if hasattr(e, 'reason'):
        print 'Theres been an error:' + e.reason
        
    
allBands = ['Bastille', 'Usher', 'Digitour', 'Watsky']
for band in allBands: 
    searchEvents('dawgtunes', 'Seattle,WA', band)