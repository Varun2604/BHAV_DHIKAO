import os, os.path
import random
import string
import json

import cherrypy

from util import ConnectionUtil

class BHAVCopy(object):
    @cherrypy.expose
    def index(self):
        return open('static/index.html')


@cherrypy.expose
class BHAVCopyService(object):

    @cherrypy.tools.accept(media='application/json')
    def GET(self, search_name='', start_index=0, count=0):
        if start_index is 0 and count is 0:
            obj = ConnectionUtil.get_instance().h_get_all(search_name)
            if obj is None:
                return json.dumps({'error' : 'invalid serach string'})
            return json.dumps(obj)
        else:



if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/generator': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    webapp = BHAVCopy()
    webapp.generator = BHAVCopyService()
    cherrypy.quickstart(webapp, '/api/', conf)