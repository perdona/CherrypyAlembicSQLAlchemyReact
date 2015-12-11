import cherrypy
from models import *
from models.customer import Customer


def log_it():
   print("Remote IP: {}".format(cherrypy.request.remote.ip))
cherrypy.tools.logit = cherrypy.Tool('before_finalize', log_it, priority=60)

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"
cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

class Root(object):
    @cherrypy.expose
    @cherrypy.tools.logit()
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        db = cherrypy.request.db
        c = Customer()
        c.name = "First Customer"
        c.order_count = 1
        db.add(c)

        cherrypy.log("bang")
        return "hello world"

    @cherrypy.expose
    def thing(self):
        cherrypy.response.headers['Content-Type'] = 'text/plain'
        def content():
            yield "Hello, "
            yield "world"
        return content()
    thing._cp_config = {'response.stream': True}

    @cherrypy.expose
    def tenjin(self):
        return {
            'page': 'tenjin.pyhtml',
            'context': {
                'msg': 'I did it with Tenjin'
            },
            'layout': None
        }

@cherrypy.popargs('name')
class Band(object):
    def __init__(self):
        self.albums = Album()

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name

@cherrypy.popargs('title')
class Album(object):
    @cherrypy.expose
    def index(self, name, title):
        return 'About %s by %s...' % (title, name)

if __name__ == '__main__':
    # ###############################################################

    # Register the SQLAlchemy plugin
    from plugins.sqlalchemy.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///my.db').subscribe()

    # Register the SQLAlchemy tool
    from plugins.sqlalchemy.satool import SATool
    cherrypy.tools.db = SATool()

    # ###############################################################

    # Register the Tenjin plugin
    from plugins.tenjin.tenjinplugin import TenjinTemplatePlugin
    TenjinTemplatePlugin(cherrypy.engine, path=["views"]).subscribe()

    # Register the Tenjin tool
    from plugins.tenjin.tenjintool import TenjinTool
    cherrypy.tools.template = TenjinTool()

    # ###############################################################

    cherrypy.config.update("configs/development.conf")

    cherrypy.tree.mount(Root(), '', {
        '/': {
            'tools.gzip.on': True,
            'tools.db.on': True,
            'tools.secureheaders.on': True,
            'tools.sessions.on': True,
            'tools.sessions.secure': True,
            'tools.sessions.httponly': True,
            'tools.template.on': True,
            'tools.encode.on': False
        }
    })

    cherrypy.tree.mount(Band(), '/band', {
        '/': {
            'tools.gzip.on': True,
            'tools.db.on': True,
            'tools.secureheaders.on': True,
            'tools.sessions.on': True,
            'tools.sessions.secure': True,
            'tools.sessions.httponly': True
        }
    })

    cherrypy.engine.start()
    cherrypy.engine.block()
