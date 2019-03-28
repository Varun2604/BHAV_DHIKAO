import os, os.path
import json
import re
from datetime import date as Date

import sys
sys.path.append(os.getcwd())

import cherrypy

from util import RedisUtil

class BHAVCopy(object):
    @cherrypy.expose
    def index(self):
        return open('web/static/index.html')

@cherrypy.expose
class BHAVCopyService(object):

    @cherrypy.tools.accept(media='application/json')
    def GET(self, date=Date.today().__str__(), name='', start_index=0, count=0):

        [yyyy, mm, dd] = re.compile('-|\/|\s').split(date)          #TODO dont fuss on date format, get universal datetime as input
        _date = Date(int(yyyy), int(mm), int(dd))

        try:
            resp = BHAVCopyService.get_data(_date, name, start_index, count)
            return json.dumps(resp)
        except InvalidServiceInput as inv_e:
            return json.dumps({'message': inv_e.__str__()})
        except Exception as e:
            print(e.with_traceback(sys.exc_info()[1]))
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
            values = RedisUtil.hm_get(_date.__str__(), name_list)
            arr = []
            for value in values:
                arr.append(json.loads(value))
            return arr


class InvalidServiceInput(Exception):
    pass


if __name__ == '__main__':
    conf = {
        '/': {
            # 'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/api': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './web/static'
        },
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000)),
        }
    }
    webapp = BHAVCopy()
    webapp.api = BHAVCopyService()
    cherrypy.quickstart(webapp, '/',config=conf)