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
    search_dict = {'app_id': id, 'location': location}
    param = urllib.urlencode(search_dict)
    search = 'http://api.bandsintown.com/events/search.json?artists[]=' + artist + '&' + param
    readEvents = urllib2.urlopen(search).read()
    eventsData = json.loads(readEvents)
    return eventsData


class Events:
    def __init__(self, data):
        self.artist = data[0]['artists'][0]['name']
        self.city = data[0]['venue']['city']
        self.state = data[0]['venue']['region']
        self.venue = data[0]['venue']['name']
        self.datetime = data[0]['datetime']
        self.ticket = data[0]['ticket_status']
        self.id = 'dawgtunes'

    def searchEvents(self, data):        
        location = self.city + ','+ self.state
        search_dict = {'app_id': 'dawgtunes', 'location': location}
        param = urllib.urlencode(search_dict)
        search = 'http://api.bandsintown.com/events/search.json?artists[]=' + self.artist + '&' + param
        try:
	        search
        except Exception:
	        print 'did not reach server'

		#eventList = []
        if len(data) == 0:
	        print '%s is not coming to %s.' % (artist, location)
        else:
	        # time_and_date = eventsData[0]['datetime']
	        # date = time_and_date[:10]
	        # time = time_and_date[11:]
	        # ticket = eventsData[0]['ticket_status']
	        # venue = eventsData[0]['venue']['name']
	        #eventList = eventList.append('%s will be in %s\n Date: %s \n Time: %s \n Ticket Status: %s \n Venue: %s' % (self.artist, self.city, self.datetime[:10], self.datetime[11:], self.ticket, self.venue))
            return '%s will be in %s\n Date: %s \n Time: %s \n Ticket Status: %s \n Venue: %s' % (self.artist, self.city, self.datetime[:10], self.datetime[11:], self.ticket, self.venue)

if __name__ == "__main__":
    #print createDict('dawgtunes', "hozier", 'Seattle,WA')
    info = createDict('dawgtunes', self.request.get('artist'), location)
    event = Events(info)        
    print event.searchEvents(info)
#createDict('dawgtunes', self.request.get("search"), 'Seattle,WA')
# event = Events(createDict('dawgtunes', "Hozier", 'Seattle,WA'))        
# print event.searchEvents()
#In app: create a for loop that will print the results in the list.

class MainHandler(webapp2.RequestHandler):
    def post(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('dawgtunes.html')
        self.response.write(template.render(template_values))

class CreateHandler(webapp2.RequestHandler):
    def post(self):
        template_values={}
        event = Events(createDict('dawgtunes', self.request.get('artist'), 'Seattle,WA'))        
        if self.request.get("artist"):
            artist = self.request.get("artist")
            method = self.request.get("method")
            location = self.request.get("location")
            #This needs to be built with the other dictionaries included: the Google Directions Api, etc. 
            #see get_photos method to use for Google Directions to include here
            template_values["search"] = artist
            results = event.searchEvents(search=artist,location=location)
            if results != None:
                template_values["results"] = results
                print results
            else:
                template_values["message"] = "Sorry, no matching results."
                template_values["results"] = ''
                print template_values["message"]
                
        else:
            template_values["message"] = "Please enter an artist to search."
            print template_values["message"]
        
        template = JINJA_ENVIRONMENT.get_template('dawgtunes_content.html')
        html = template.render(template_values)
        self.response.write(html)
        # fname = "dawgtunes_content.html"
        # f = open(fname, 'w')
        # f.write(html)
        # f.close()

application = webapp2.WSGIApplication([\
                                    ('/', MainHandler),
                                    ('/dawgtunes_content.html', CreateHandler),
                                    ('/dawgtunes_request.html', PostHandler)
                                    ], debug=True)