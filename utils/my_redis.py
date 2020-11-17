from redis import Redis
import pickle
import sys


class RedisDB:
    def __init__(self):
        self.redis = Redis(host="10.10.20.50", port=6379, db=0)

    def write(self, key, val):
        try:
            self.redis.set(key, pickle.dumps(val))
            return True
        except Exception:
            err = sys.exc_info()
            if __debug__:
                print("Redis._write: ", err, err[-1].tb_lineno)
            return False

    def read(self, key):
        try:
            rs = self.redis.get(key)
            if rs:
                return pickle.loads(rs)
        except Exception:
            err = sys.exc_info()
            if __debug__:
                print("Redis._write: ", err, err[-1].tb_lineno)
            return False

    def delete(self, key):
        try:
            self.redis.delete(key)
            return True
        except Exception:
            err = sys.exc_info()
            if __debug__:
                print("Redis._write: ", err, err[-1].tb_lineno)
            return False

    def get_data(self, key):
        data = None
        try:
            d = self.redis.get(key)
            if d:
                data = pickle.loads(d)
                self.redis.delete(key)
        except Exception:
            err = sys.exc_info()
            if __debug__:
                print("Redis._get_data: ", err, err[-1].tb_lineno)
        finally:
            return data

r = RedisDB()
print(r.read('77000211021'))