import os, os.path
import random
import string
import json

import cherrypy

from util import RedisConnection

class BHAVCopy(object):
    @cherrypy.expose
    def index(self):
        return open('static/index.html')


@cherrypy.expose
class BHAVCopyService(object):

    @cherrypy.tools.accept(media='application/json')
    def GET(self, date, search_name='', start_index=0, count=0):
        if start_index is 0 and count is 0:
            obj = RedisConnection.hget_all(search_name+':'+date)
            if obj is None:
                return json.dumps({'error' : 'invalid search string'})
            return json.dumps(obj)
        else:
            list = RedisConnection.l_range('ordered_list'+':'+date, start_index, count)
            arr = []
            for name in list:
                obj = RedisConnection.h_get(date, name)
                obj = json.load(obj)
                arr.append(obj)
            return json.dumps(arr)



if __name__ == '__main__':
    # conf = {
    #     '/': {
    #         'tools.sessions.on': True,
    #         'tools.staticdir.root': os.path.abspath(os.getcwd())
    #     },
    #     '/generator': {
    #         'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
    #         'tools.response_headers.on': True,
    #         'tools.response_headers.headers': [('Content-Type', 'text/plain')],
    #     },
    #     '/static': {
    #         'tools.staticdir.on': True,
    #         'tools.staticdir.dir': './public'
    #     }
    # }
    webapp = BHAVCopy()
    webapp.generator = BHAVCopyService()
    cherrypy.quickstart(webapp, '/api/')