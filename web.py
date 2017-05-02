import cherrypy
import configparser
from jinja2 import Environment, FileSystemLoader


class WebApplication(object):
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader('templates'))
    @cherrypy.expose
    def index(self, dataisset=None):
        # Render the user interface and return it to the browser.
        if dataisset == "true":
            cherrypy.session['dataisset']=dataisset
        template = self.env.get_template('index.html')
        return template.render(title='<b>Polling</b><i>Balance</i>', plaintitle="Polling Balance",dataisset=cherrypy.session.get('dataisset'))
cherrypy.config.update({'tools.sessions.on': True})
cherrypy.quickstart(WebApplication())