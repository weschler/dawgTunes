import os, urllib, urllib2, json, logging
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

def pretty(obj):
    return json.dumps(obj, sort_keys=True, indent=2)


def safeGet(url):
    try:
        return urllib2.urlopen(url)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        return None

def createDict(id, artist, location):
		search_dict = {'app_id': id, 'artist': artist, 'location': location}
		param = urllib.urlencode(search_dict)
		search = 'http://api.bandsintown.com/events/search.json?artists[]=' + param
		readEvents = urllib2.urlopen(search)
		eventsData = json.loads(readEvents)
		return eventsData


class Events:
	def __init__(self, data):
		#why does it keep saying that data is not defined?
		self.artist = data['artists']['name']
        self.city = data['venue']['city']
        self.state = data['venue']['region']
        self.venue = data['venue']['name']
        self.datetime = data['datetime']
        self.ticket = data['ticket_status']
        self.id = 'dawgtunes'

	def searchEvents(self):
	     try:
	         readEvents = urllib2.urlopen(createURL(self.id, self.city + ','+ self.state, self.artist)).read()
	     except Exception:
	         print 'did not reach server'
	    eventList = []
	    if len(data) == 0:
	        print '%s is not coming to %s.' % (artist, location)
	    else:
	        # time_and_date = eventsData[0]['datetime']
	        # date = time_and_date[:10]
	        # time = time_and_date[11:]
	        # ticket = eventsData[0]['ticket_status']
	        # venue = eventsData[0]['venue']['name']
	        newList = eventList.append('%s will be in %s\n Date: %s \n Time: %s \n Ticket Status: %s \n Venue: %s' % (self.artist, self.city, self.datetime[:10], self.datetime[11:], self.ticket, self.venue))
	        return newList

event = Events(createDict('dawgtunes', 'hozier', 'Seattle,WA'))		   
print event.searchEvents()
#In app: create a for loop that will print the results in the list.

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('dawgtunes.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        template_values={}
        if self.request.get("search",False):
            search = self.request.get("search")
            method = self.request.get("method")
            #This needs to be built with the other dictionaries included: the Google Directions Api, etc. 
            #see get_photos method to use for Google Directions to include here
            template_values["query"] = search
            results = searchEvents(search=search,method=method)
            if results != None:
                template_values["results"] = results
            else:
                template_values["message"] = "Sorry, no matching results."
                template_values["results"] = []
                
        else:
            template_values["message"] = "Please enter one or more tags for which to search."
        
        template = JINJA_ENVIRONMENT.get_template('dawgtunes.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)