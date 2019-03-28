import redis

from config import Config
config = Config.get_config()

class RedisUtil:
    connection = None

    @staticmethod
    def get_redis_connection():
        if RedisUtil.connection is None:
            RedisUtil.connection = redis.Redis(**config.REDIS_CONNECTION_DETAILS)
        return RedisUtil.connection

    @staticmethod
    def hm_set(hash, obj):
        RedisUtil.get_redis_connection().hmset(hash, obj)

    @staticmethod
    def hget_all(hash):
        obj = RedisUtil.get_redis_connection().hgetall(hash)
        if obj is None:
            return None
        response = {}
        for key in obj.keys():
            response[key.decode('utf-8')] = obj[key].decode('utf-8')
        return response

    @staticmethod
    def h_get(hash, key):
        value = RedisUtil.get_redis_connection().hget(hash, key)
        if value is None:
            return ''
        return value.decode('utf-8')

    @staticmethod
    def hm_get(hash, keys):
        arr = RedisUtil.get_redis_connection().hmget(hash, keys)
        ret = []
        for b_str in arr:
            ret.append(b_str.decode('utf-8'))
        return ret

    @staticmethod
    def r_push(list_name, list):
        RedisUtil.get_redis_connection().rpush(list_name, *list)

    @staticmethod
    def l_push(list_name, list):
        RedisUtil.get_redis_connection().lpush(list_name, *list)

    @staticmethod
    def keys(pattern='*'):
        return RedisUtil.get_redis_connection().keys(pattern)

    @staticmethod
    def l_range(list_name, start_index, count):
        list = RedisUtil.get_redis_connection().lrange(list_name, start_index, count)
        if list is None or len(list) is 0:
            return []
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list
