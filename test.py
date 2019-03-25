import cherrypy
import redis
import json

class HelloWorld(object):
    r = redis.Redis(host='localhost', port=6379, db=0)
    @cherrypy.expose
    def index(self):
        return "Hello world!"
    @cherrypy.expose
    def test(self, name="", count=10):
        obj = HelloWorld.r.hgetall(name)
        response = {}
        for key in obj.keys():
            response[key.decode('utf-8')] = obj[key].decode('utf-8')
        return json.dumps(response)

if __name__ == '__main__':
    cherrypy.quickstart(HelloWorld())
