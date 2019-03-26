import csv
import redis
import json

from config import Config
config = Config.get_config()



# file_name - name of file
# date - date in the format - YYYY-MM-DD
def populate_data(file_name, date):
    f = open(file_name+".CSV", "r")
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        name = row['SC_NAME'].strip()
        obj = {
            'code' : row['SC_CODE'].strip(),
            'name': row['SC_NAME'].strip(),
            'open': row['OPEN'].strip(),
            'high': row['HIGH'].strip(),
            'low': row['LOW'].strip(),
            'close': row['CLOSE'].strip()
        }
        # ConnectionUtil.hm_set(name+':'+date, obj)
        x = {}
        x[name]=json.dumps(obj)
        ConnectionUtil.hm_set(date, x)
        ConnectionUtil.r_push('ordered_list'+':'+date,name)

class ConnectionUtil:
    connection = None

    @staticmethod
    def get_redis_connection():
        if ConnectionUtil.connection is None:
            ConnectionUtil.connection = redis.Redis(host=config.REDIS_CONNECTION_DETAILS['host'],
                                                    port=config.REDIS_CONNECTION_DETAILS['port'],
                                                    db=config.REDIS_CONNECTION_DETAILS['db'])
        return ConnectionUtil.connection

    @staticmethod
    def hm_set(hash, obj):
        ConnectionUtil.get_redis_connection().hmset(hash, obj)

    @staticmethod
    def hget_all(hash):
        obj = ConnectionUtil.get_redis_connection().hgetall(hash)
        if obj is None:
            return None
        response = {}
        for key in obj.keys():
            response[key.decode('utf-8')] = obj[key].decode('utf-8')
        return response

    @staticmethod
    def h_get(hash, key):
        return ConnectionUtil.get_redis_connection().hget(hash, key)

    @staticmethod
    def r_push(list_name, obj):
        ConnectionUtil.get_redis_connection().rpush(list_name, obj)

    @staticmethod
    def l_push(list_name, obj):
        ConnectionUtil.get_redis_connection().lpush(list_name, obj)
        
    @staticmethod
    def l_range(list_name, start_index, count):
        list = ConnectionUtil.get_redis_connection().lrange(list_name, start_index, count)
        if list is None:
            return None
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list
