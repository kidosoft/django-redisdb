#######
Redisdb
#######

.. image:: https://pypip.in/wheel/django-redisdb/badge.svg
    :target: https://pypi.python.org/pypi/django-redisdb/
    :alt: Wheel Status

.. image:: https://pypip.in/version/django-redisdb/badge.svg
    :target: https://pypi.python.org/pypi/django-redisdb/
    :alt: Latest Version

.. image:: https://pypip.in/license/django-redisdb/badge.svg
    :target: https://pypi.python.org/pypi/django-redisdb/
    :alt: License

.. image:: https://travis-ci.org/kidosoft/django-redisdb.svg?branch=master
    :target: https://travis-ci.org/kidosoft/django-redisdb
    :alt: Build status

.. image:: https://coveralls.io/repos/kidosoft/django-redisdb/badge.svg
    :target: https://coveralls.io/r/kidosoft/django-redisdb
    :alt: Coverage

.. image:: https://readthedocs.org/projects/django-redisdb/badge/?format=svg
    :target: https://django-redisdb.readthedocs.org
    :alt: Documetation


Django-redisdb is Redis backend for Django that allows 
using Redis as a cache and as a database at the same time.
Django-redisdb provides backends for master/master and sharded configuration.

Installation
============

.. code-block:: console

   pip install django-redisdb

Quick usage guide
=================


In settings.py:

.. code-block:: python

    CACHES = {
        'redis_ring': {
            'BACKEND': 'redisdb.backends.RedisRing',  # sharding backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ],
        },
        'redis_copy': {
            'BACKEND': 'redisdb.backends.RedisCopy',  # copying backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ],
        }
    }

Usage:

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
For example you can use redis' sorted sets:

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


Supported Django versions
=========================

django-redisdb runs on Django 1.2 to Django 1.8

Documentation
=============

Full documentation is available at http://django-redisdb.readthedocs.org
