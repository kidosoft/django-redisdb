.. _configuration:

Configuration
=============

django-redisdb is configured using standard Django's cache framework:

.. code-block:: python

    CACHES = {
        'redis_ring': {
            'BACKEND': 'redisdb.backends.RedisRing',  # sharding backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ],
            'OPTIONS': {
                'socket_timeout': 5,
                'socket_connect_timeout': 5,
            },
        },
        'redis_copy': {
            'BACKEND': 'redisdb.backends.RedisCopy',  # copying backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ],
            'OPTIONS': {
                'socket_timeout': 5,
                'socket_connect_timeout': 5,
            },
        }
    }


Required key's are:

* BACKEND - :py:class:`redisdb.backends.RedisRing` or :py:class:`redisdb.backends.RedisCopy`.
  It determines how data would be stored across nodes.
* DB - database identifier number
* LOCATION - list of node addresses


You can pass additional options for connection creation :

* password - password for authentication
* socket_timeout - timeout for blocking operations
* socket_connect_timeout - timeout on connection
* retry_on_timeout - if True, retry when timeout occured

