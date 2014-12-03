import urllib, urllib2, json, datetime


def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)

def createURL(origin, destination, time, mode):
    api_key = 'AIzaSyCEJi_xLwrrX57fOTziF-bTO7l_yOb32RU'
    base = 'https://maps.googleapis.com/maps/api/directions/json?origin=' + origin + '&destination=' + destination + '&key=' + api_key + '&departure_time=' + time + '&mode=' + mode 
    return base

# print to test out whether the code is working properly 
#print createURL(origin= 'Brooklyn', destination= 'Queens', time='1343641500', mode='transit')

def searchDirections(origin, destination, time, mode):
     try:
         readDirections = urllib2.urlopen(createURL(origin, destination, time, mode)).read()
     except Exception:
         print 'did not reach server'


     directionData = json.loads(readDirections)
     if len(directionData) == 0:
         print '%s could not be found.' % (destination)
     else:
        distance = directionData['routes'][0]['legs'][0]['distance']['text']
        print 'The %s is %s away from %s by %s.' % (origin, distance, destination, mode)

   
searchDirections('Brooklyn','Queens', '1343641500', 'transit')

try:
    urllib2.urlopen(createURL('Brooklyn','Queens', '1343641500', 'transit'))
except urllib2.URLError, e:
    if hasattr(e, 'reason'):
        print 'Theres been an error:' + e.reason
        
    
allMode = ['transit', 'walking', 'driving', 'bicycling']
for mode in allMode: 
    searchDirections('Brooklyn','Queens', '1343641500', mode)

        
            # if 'arrival_time' in directionData['routes'][0]['legs'][0]:
            #     arrvial_time = directionData['routes'][0]['legs'][0]['arrvial_time']['text']
            #     print 'You will arrive at %s.' % (arrvial_time)
            # elif 'distance' in directionData['routes'][0]['legs'][0]:       
            #     distance = directionData['routes'][0]['legs'][0]['distance']['text']
            #     print 'The place is %s away.' % (distance)

#NOTE: convert time to epochtime 