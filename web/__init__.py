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

class Api(object):

    def __init__(self):
        self.bhav_data = BhavData()
        self.available_dates = AvailableDates()

    def _cp_dispatch(self, vpath):
        try:
            if len(vpath) > 0:
                entity_name = vpath.pop()
                if entity_name == 'data':
                    return self.bhav_data
                elif entity_name == 'available_dates':
                    return self.available_dates
        except BaseException as e:
            print(e.with_traceback(sys.exc_info()[1]))

    @cherrypy.expose
    def index(self, name):
        return 'About %s...' % name



@cherrypy.expose
class BhavData(object):

    @cherrypy.tools.accept(media='application/json')
    def GET(self, date=Date.today().__str__(), name='', start_index=0, count=0):

        [yyyy, mm, dd] = re.compile('-|\/|\s').split(date)          #TODO dont fuss on date format, get universal datetime as input
        _date = Date(int(yyyy), int(mm), int(dd))

        try:
            resp = BhavData.get_data(_date, name, start_index, count)
            return json.dumps(resp)
        except InvalidInput as inv_e:
            raise cherrypy.HTTPError(404, json.dumps({'message': inv_e.__str__()}))
        except Exception as e:
            print(e.with_traceback(sys.exc_info()[1]))
            raise cherrypy.HTTPError(404, json.dumps({'message': 'Unknown Error'}))


    @staticmethod
    def get_data(_date, name, start_index, count):
        if start_index is 0 and count is 0:
            result = RedisUtil.h_get(_date.__str__(), name)
            if result is None or result is '':
                raise InvalidInput('Invalid input - Search string or Date')
            return json.loads(result)
        else:
            name_list = RedisUtil.l_range(_date.__str__()+'_name_list', start_index, count)
            values = RedisUtil.hm_get(_date.__str__(), name_list)
            arr = []
            for value in values:
                arr.append(json.loads(value))
            return arr

@cherrypy.expose
class AvailableDates(object):
    @cherrypy.tools.accept(media='application/json')
    def GET(self):
        try:
            dates_list = RedisUtil.l_range('available_dates', 0, -1)                # fetch all dates available
            return json.dumps(dates_list)
        except InvalidInput as inv_e:
            return json.dumps({'message': inv_e.__str__()})
        except Exception as e:
            print(e.with_traceback(sys.exc_info()[1]))
            return json.dumps({'message': 'Unknown Error'})


class InvalidInput(Exception):
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
    webapp.api = Api()
    # webapp.api = {
    #     'bhav' : BhavData(),
    #     'available_dates' : AvailableDates()
    # }
    # webapp.api.bhav = BhavData()
    # webapp.api.available_dates = AvailableDates()
    cherrypy.quickstart(webapp, '/',config=conf)