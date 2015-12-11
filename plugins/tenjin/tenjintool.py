import cherrypy
import tenjin
from tenjin.helpers import *

__all__ = ['TenjinTool']

class TenjinTool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'before_finalize',
                               self._render,
                               priority=10)

    def _render(self, debug=False):
        # retrieve the data returned by the handler
        data = cherrypy.response.body or {}
        engine = cherrypy.engine.publish("lookup-engine").pop()

        if isinstance(data, dict) and data.get('page', None) and data.get('context', None):
            cherrypy.response.body = engine.render(data.get('page'), data.get('context'), data.get('layout')).encode(cherrypy.response.headers.encodings[0])
