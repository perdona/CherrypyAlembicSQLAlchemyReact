import cherrypy
from cherrypy.process import plugins
import tenjin
from tenjin.helpers import *

__all__ = ['TenjinTemplatePlugin']

class TenjinTemplatePlugin(plugins.SimplePlugin):
    """A WSPBus plugin that manages Tenjin templates"""

    def __init__(self, bus, path, postfix=".pyhtml", layout=None):
        plugins.SimplePlugin.__init__(self, bus)
        self.path = path
        self.postfix = postfix
        self.layout = layout

    def start(self):
        """
        Called when the engine starts.
        """
        self.bus.log('Setting up Tenjin resources')
        self.bus.subscribe("lookup-engine", self.get_engine)

    def stop(self):
        """
        Called when the engine stops.
        """
        self.bus.log('No Tenjin resources')
        self.bus.unsubscribe("lookup-engine", self.get_engine)
        self.paths = None

    def get_engine(self):
        return tenjin.Engine(path=self.path, postfix=self.postfix, layout=self.layout)

