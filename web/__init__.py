import os, os.path
import random
import string
import json
from datetime import date

import sys
# print(os.getcwd())
sys.path.append(os.getcwd())
# print(sys.path)

import cherrypy

import config
from util import RedisUtil

class BHAVCopy(object):
    @cherrypy.expose
    def index(self):
        return open('web/static/index.html')


@cherrypy.expose
class BHAVCopyService(object):

    @cherrypy.tools.accept(media='application/json')
    def GET(self, date, search_str='', start_index=0, count=0):

        [dd, mm, yyyy] = date.split('-/\s')
        _date = date(int(yyyy), int(mm), int(dd))

        try:
            resp = BHAVCopyService.get_data(_date, search_str, start_index, count)
            return json.dumps(resp)
        except InvalidServiceInput as inv_e:
            return json.dumps({'message': inv_e.__str__()})
        except Exception:
            return json.dumps({'message': 'Unknown Error'})


    @staticmethod
    def get_data(_date, name, start_index, count):
        if start_index is 0 and count is 0:
            result = RedisUtil.h_get(_date.__str__(), name)
            if result is None or result is '':
                raise InvalidServiceInput('Invalid input - Search string or Date')
            return json.loads(result)
        else:
            name_list = RedisUtil.l_range(_date.__str__()+'_name_list', start_index, count)
            arr = []
            for name in name_list:
                obj = RedisUtil.h_get(_date.__str__(), name)
                obj = json.load(obj)
                arr.append(obj)
            return json


class InvalidServiceInput(Exception):
    pass


if __name__ == '__main__':
    conf = {
        # '/': {
        #     'tools.sessions.on': True,
        #     'tools.staticdir.root': os.path.abspath(os.getcwd())
        # },
        # '/generator': {
        #     'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
        #     'tools.response_headers.on': True,
        #     'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        # },
        # '/static': {
        #     'tools.staticdir.on': True,
        #     'tools.staticdir.dir': './public'
        # }
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
        }
    }
    webapp = BHAVCopy()
    webapp.generator = BHAVCopyService()
    cherrypy.quickstart(webapp, '/api/',config=conf)