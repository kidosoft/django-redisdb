Quick usage quide
=================

If you configured connection :ref:`configuration` you can use Redis like
any other Django's cache:

.. code-block:: python

   >>> from django.core.cache import caches
   >>> caches['redis_ring'].set('one_key', 123)  # set key1 only on on server
   [True]
   >>> caches['redis_copy'].set('other_key', 234)  # set key2 on all servers
   [True, True]

With RedisRing value is set only on one node. With RedisCopy it's set on all
nodes (two nodes in examle above).

Redis is much more powerfull then simple cache. It should be seen
as a specialized database. With django-redisdb you can use all its power.
For example you can use redis' sorted sets [#SORTEDSETS]_:

.. code-block:: python

    >>> caches['redis_copy'].zadd('myzset', 1, 'one')
    [0, 1]
    >>> caches['redis_copy'].zadd('myzset', 2, 'two')
    [0, 1]
    >>> caches['redis_copy'].zadd('myzset', 3, 'three')
    [0, 1]
    >>> caches['redis_copy'].zrange('myzset', 0, -1)
    ['one', 'two', 'three']
    >>> caches['redis_copy'].zrange('myzset', 0, -1, withscores=True)
    [('one', 1.0), ('two', 2.0), ('three', 3.0)]

Return values
-------------

RedisCopy can save data to many nodes. Each of this nodes can return different
result on save. For that reason commands that save data to nodes returns list
of results from each node. E.g. with two nodes set for redis_copy:

.. code-block:: python

   >>> print caches['redis_copy'].set('key1', 2)
   [True, True]


.. [#SORTEDSETS] Sorted sets http://redis.io/commands/zrange
