import webapp2, os, urllib, urllib2, json, logging
import jinja2
import myflickr_key

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

class Events:
	def __init__(self, search):
		self.


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values={}
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))
        
    def post(self):
        template_values={}
        
        if self.request.get("tags",False):
            tags = self.request.get("tags")
            mode = self.request.get("mode")
            template_values["query"] = tags
            results = get_photos(tags=tags,mode=mode)
            if results != None:
                template_values["photos"] = results
            else:
                template_values["message"] = "Sorry, no matching results."
                template_values["photos"] = []
                
        else:
            template_values["message"] = "Please enter one or more tags for which to search."
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)