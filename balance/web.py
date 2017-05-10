import cherrypy
import configparser
import json
from abc import ABCMeta, abstractmethod
from jinja2 import Environment, FileSystemLoader

class BalanceJSONSerializable:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_json(self):
        pass


class BalanceJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BalanceJSONSerializable):
            return obj.to_json()
        else:
            return super().default(obj)

    def iterencode(self, value):
        for chunk in super().iterencode(value):
            yield chunk.encode('utf-8')

# Custom json_handler which should be extended as needed to allow custom serialization of objects.
def json_handler(*args, **kwargs):
    value = cherrypy.serving.request._json_inner_handler(*args, **kwargs)
    return WebApplication.json_encoder.iterencode(value)

class WebApplication(object):
    json_encoder = BalanceJSONEncoder()
    def __init__(self):
        # Read the tempo config file to initialize the web application.
        self.config = configparser.ConfigParser()
        self.config.read("cfg/balance.cfg")

        # Configure cherrypy to use our custom JSON handler.
        cherrypy.config['tools.json_out.handler'] = json_handler

        # Set the environment
        self.env = Environment(loader=FileSystemLoader('templates'))
        # Start the web server using the cherrypy config file.
        cherrypy.config.update({'tools.sessions.on': True})
        cherrypy.quickstart(self, "", "cfg/cherrypy.cfg")


    @cherrypy.expose
    def index(self, dataisset=None):
        # Render the user interface and return it to the browser.

        template = self.env.get_template('index.html')
        return template.render(title='<b>Polling</b><i>Balance</i>', plaintitle="Polling Balance")

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def requestdata(self,name):
        if name=="MUP48":
            with open('./static/data/MUP48.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data
        elif name=="All_Adults":
            with open('./static/data/All_Adults.json') as data_file:
                data = json.load(data_file)
                cherrypy.response.headers['Content-Type'] = 'application/json'
                return data





