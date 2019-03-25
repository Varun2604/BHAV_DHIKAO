import csv
import redis

def populate_data(file_name):
    f = open(file_name+".CSV", "r")
    csv_reader = csv.DictReader(f)
    redis_connection = ConnectionUtil.get_instance().get_redis_connection()
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
        redis_connection.hmset(name, obj)
        redis_connection.rpush('ordered_list',name)

class ConnectionUtil:
    connection = None

    @staticmethod
    def get_redis_connection():
        if ConnectionUtil.connection is None:
            ConnectionUtil.connection = redis.Redis(host='localhost', port=6379, db=0)
        return ConnectionUtil.connection

    @staticmethod
    def hm_set(hash, obj):
        ConnectionUtil.get_redis_connection().hmset(hash, obj)

    @staticmethod
    def hget_all(name):
        obj = ConnectionUtil.get_redis_connection().hgetall(name)
        if obj is None:
            return None
        response = {}
        for key in obj.keys():
            response[key.decode('utf-8')] = obj[key].decode('utf-8')
        return response

    @staticmethod
    def r_push(list_name, obj):
        ConnectionUtil.get_redis_connection().rpush(list_name, obj)
        
    @staticmethod
    def l_range(list_name, start_index, count):
        list = ConnectionUtil.get_redis_connection().lrange(list_name, start_index, count)
        if list is None:
            return None
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list
