# -*- coding: utf-8 -*-

""" Backends which simplify access to redis through django cache framework. """

__doc__ = """
Backends
========
"""


from django.core.cache.backends.base import BaseCache
import hash_ring
import redis


class ConstRedis(redis.StrictRedis):

    """ Redis client that adds consistent hashing to :py:mod:`redis:StrictRedis`. """

    def __init__(self, *args, **kwargs):
        self.hash_key = kwargs.pop('hash_key', 1)
        super(ConstRedis, self).__init__(*args, **kwargs)

    def __hash__(self):
        return self.hash_key

    def __str__(self):
        return '%s' % self.hash_key

    def close(self):
        # required by django interface but not used
        pass  # pragma: no cover


class AbstractRedis(BaseCache):

    def __init__(self, location, params):
        self.db = params.pop('DB')
        options = params.pop('options', {})
        super(AbstractRedis, self).__init__(params)
        self.create_nodes(location, **options)

    def create_nodes(self, location, **options):
        """ Create connections to redis nodes.

        @param str location: host:port indicating redis node location.
        @param dict options: redis options
        """
        nodes = []
        for i, node in enumerate(location):
            host, port = node.rsplit(':', 1)
            redis_pool = redis.ConnectionPool(host=host, port=port, db=self.db, **options)
            nodes.append(ConstRedis(connection_pool=redis_pool, hash_key=i, **options))
        self.nodes = nodes
        self.nodes_ring = hash_ring.HashRing(nodes)


WRITE_COMMANDS = [
    'append',
    'bitop',
    'blpop',
    'brpop',
    'brpoplpush',
    'decr',
    'decrby',
    'del',
    'expire',
    'expireat',
    'flushall',
    'flushdb',
    'getset',
    'hdel',
    'hincrby',
    'hincrbyfloat',
    'hmset',
    'hset',
    'hsetnx',
    'incr',
    'incrby',
    'incrbyfloat',
    'linsert',
    'lpop',
    'lpush',
    'lpushx',
    'lrem',
    'lset',
    'ltrim',
    'mset',
    'msetnx',
    'persist',
    'pexpire',
    'pexpireat',
    'pfadd',
    'psetex',
    'rename',
    'renamenx',
    'rpop',
    'rpoplpush',
    'rpush',
    'rpushx',
    'sadd',
    'sdiffstore',
    'set',
    'setbit',
    'setex',
    'setnx',
    'setrange',
    'sinterstore',
    'smove',
    'sort',
    'spop',
    'srem',
    'sunionstore',
    'zadd',
    'zincrby',
    'zinterstore',
    'zrem',
    'zremrangebylex',
    'zremrangebyrank',
    'zremrangebyscore',
    'zunionstore',
]


class RedisRing(AbstractRedis):

    """ RedisRing backend which writes only to one Redis server based on key.

    RedisRing is only a proxy to underlying :py:class:`ConstRedis` objects, which represents
    each Redis instance. It has the same methods set as :py:class:`ConstRedis`.
    Individual nodes can be accessed through `nodes` attribute.

    RedisRing is better suited for using Redis as memcached replacement.
    With one server failure data kept on that server have to be recreated.
    """

    def __getattribute__(self, name):
        """ Proxy for StrictRedis attributes. """
        if name in ['create_nodes', 'nodes', 'nodes_ring', 'db']:
            return object.__getattribute__(self, name)

        def wrapper(*args, **kwargs):
            try:
                key = args[0]
            except IndexError:
                key = ''
            node = self.nodes_ring.get_node(key)
            func = getattr(node, name)
            return func(*args, **kwargs)
        return wrapper


class RedisCopy(AbstractRedis):

    """ Redis backend which writes to all Redis servers.

    RedisCopy is only a proxy to underlying :py:class:`ConstRedis` objects, which represents
    each Redis instance. It has the same methods set as :py:class:`ConstRedis`.
    Individual nodes can be accessed through `nodes` attribute.

    Fetching is done only from one server based on key just like in RedisRing.
    RedisCopy can be seen like master/master configuration
    where synchronization isn't done by Redis itself but by clients.
    It's well suited for storing data that should be available
    even if one server goes down.
    """

    def __getattribute__(self, name):
        """ Proxy for StrictRedis attributes. """
        if name in ['create_nodes', 'nodes', 'nodes_ring', 'db']:
            return object.__getattribute__(self, name)

        def wrapper(*args, **kwargs):
            try:
                key = args[0]
            except IndexError:
                key = ''
            if name not in WRITE_COMMANDS:
                node = self.nodes_ring.get_node(key)
                func = getattr(node, name)
                return func(*args, **kwargs)
            else:
                results = []
                for node in self.nodes:
                    func = getattr(node, name)
                    results.append(func(*args, **kwargs))
                return results
        return wrapper


__all__ = ('RedisCopy', 'RedisRing')
