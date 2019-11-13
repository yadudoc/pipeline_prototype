import redis

class ValueServer:
    def __init__(self, hostname, port=6379, database=0):
        """ Initialize
        """
        self.hostname = hostname
        self.port = port
        self.redis_client = None
        self.database = database

    #def connect(self):
        """ Connects to the Redis server
        """
        try:
            if not self.redis_client:
                self.redis_client = redis.StrictRedis(host=self.hostname, port=self.port, db=self.database, decode_responses=True)
        except redis.exceptions.ConnectionError:
            print("ConnectionError while trying to connect to Redis@{}:{}".format(self.hostname,
                                                                                  self.port))
            raise

    def set(self, key, value):
        print('value_server set', key, value)
        self.redis_client.set(key, value)

    def get(self, key):
        v = self.redis_client.get(key)
        print('Get returns', v)
        return( self.redis_client.get(key) )

    def size(self):
        n = self.redis_client.dbsize()
        print('Size is',n)
        return(self.redis_client.dbsize())

    def flush(self):
        return(self.redis_client.flushdb())

    def all_keys(self):
        return( self.redis_client.keys() )
