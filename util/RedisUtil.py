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
    def h_scan(list_name, search_string, search_till_end=False, total_count=10):
        response = {}
        search = True
        cursor = 0

        while search:
            res = RedisUtil.get_redis_connection().hscan(list_name, match=search_string, cursor=cursor, count=10)
            cursor = res[0]
            objs = res[1]
            if len(objs) > 0:
                for key in objs:
                    response[key.decode('utf-8')] = objs[key].decode('utf-8')
                    if len(response) == total_count:
                        break
                search = not ( total_count >= len(response) ) and search_till_end
            if cursor is 0:
                search = False

        return response

    @staticmethod
    def r_push(list_name, list):
        RedisUtil.get_redis_connection().rpush(list_name, *list)

    @staticmethod
    def l_push(list_name, list):
        RedisUtil.get_redis_connection().lpush(list_name, *list)

    @staticmethod
    def l_range(list_name, start_index, count):
        list = RedisUtil.get_redis_connection().lrange(list_name, start_index, count)
        if list is None or len(list) is 0:
            return []
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list

    @staticmethod
    def s_add(set_name, set):
        RedisUtil.get_redis_connection().sadd(set_name, *set)

    @staticmethod
    def s_members(set_name):
        list = RedisUtil.get_redis_connection().smembers(set_name)
        if list is None or len(list) is 0:
            return []
        response_list = []
        for item in list:
            response_list.append(item.decode('utf-8'))
        return response_list

    @staticmethod
    def s_ismember(set_name, key):
        return RedisUtil.get_redis_connection().sismember(set_name, key)

    @staticmethod
    def keys(pattern='*'):
        return RedisUtil.get_redis_connection().keys(pattern)