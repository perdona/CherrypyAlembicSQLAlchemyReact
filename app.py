import cherrypy

def log_it():
   print("Remote IP: {}".format(cherrypy.request.remote.ip))
cherrypy.tools.logit = cherrypy.Tool('before_finalize', log_it)

def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"
cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

class Root(object):
    @cherrypy.expose
    def index(self):
        # Get the SQLAlchemy session associated
        # with this request.
        # It'll be released once the request
        # processing terminates
        db = cherrypy.request.db

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
    # Register the SQLAlchemy plugin
    from plugins.sqlalchemy.saplugin import SAEnginePlugin
    SAEnginePlugin(cherrypy.engine, 'sqlite:///my.db').subscribe()

    # Register the SQLAlchemy tool
    from plugins.sqlalchemy.satool import SATool
    cherrypy.tools.db = SATool()

    cherrypy.config.update("configs/development.conf")

    cherrypy.tree.mount(Root(), '', {
        '/': {
            'tools.gzip.on': True,
            'tools.db.on': True,
            'tools.secureheaders.on': True,
            'tools.sessions.on': True,
            'tools.sessions.secure': True,
            'tools.sessions.httponly': True
        }
    })

    cherrypy.tree.mount(Band(), '/band', {
        '/band': {
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
