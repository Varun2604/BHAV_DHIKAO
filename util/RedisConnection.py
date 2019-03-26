import redis

from config import Config
config = Config.get_config()

class RedisConnection:
    connection = None

    @staticmethod
    def get_redis_connection():
        if RedisConnection.connection is None:
            RedisConnection.connection = redis.Redis(host=config.REDIS_CONNECTION_DETAILS['host'],
                                                    port=config.REDIS_CONNECTION_DETAILS['port'],
                                                    db=config.REDIS_CONNECTION_DETAILS['db'])
        return RedisConnection.connection

    @staticmethod
    def hm_set(hash, obj):
        RedisConnection.get_redis_connection().hmset(hash, obj)

    @staticmethod
    def hget_all(hash):
        obj = RedisConnection.get_redis_connection().hgetall(hash)
        if obj is None:
            return None
        response = {}
        for key in obj.keys():
            response[key.decode('utf-8')] = obj[key].decode('utf-8')
        return response

    @staticmethod
    def h_get(hash, key):
        return RedisConnection.get_redis_connection().hget(hash, key)

    @staticmethod
    def r_push(list_name, obj):
        RedisConnection.get_redis_connection().rpush(list_name, obj)

    @staticmethod
    def l_push(list_name, obj):
        RedisConnection.get_redis_connection().lpush(list_name, obj)

    @staticmethod
    def l_range(list_name, start_index, count):
        list = RedisConnection.get_redis_connection().lrange(list_name, start_index, count)
        if list is None:
            return None
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list
