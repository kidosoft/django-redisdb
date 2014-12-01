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


Goal
====

Provide Redis backends for Django that faciliates using multiple Redis servers
in the same time like if they were in master/master or sharded configuration.

Installation
============

Install requirements:

.. code-block:: console
    
    pip install -r requirements.txt

Install Redisdb:

.. code-block:: console

   pip install django-redisdb

or current development version:

.. code-block:: console

   pip install hg+https:://bitbucket.org/kidosoft/django-redisdb

Configuration
=============

.. code-block:: python

    CACHES = {
        'redis_ring': {
            'BACKEND': 'redisdb.backends.RedisRing',  # sharding backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ]
        },
        'redis_copy': {
            'BACKEND': 'redisdb.backends.RedisCopy',  # copying backend
            'DB': 0,
            'LOCATION': [
                'localhost:6379',
                'localhost:6380',
            ]
        }
    }


Redis is configured as cache backend although it should be treat as specialized
database. There are two backends:

Usage
=====

After configuration access to Redis is done like to any other Django cache:

.. code-block:: python

   from django.core.cache import caches
   caches['redis_ring'].set('key1', 1)  # set key1 only on on server
   caches['redis_copy'].set('key2', 2)  # set key2 on all servers
   result_list = caches['redis_copy'].zrange('key3', 1, 10)  # redis only command

Caveats 
=======

RedisCopy can save data to many nodes. Each of this nodes can return different
result on save. For that reason commands that save data to nodes returns list
of results from each node. E.g. with two nodes set for redis_copy:

.. code-block:: python

   >>> print caches['redis_copy'].set('key1', 2)
   [True, True]

Supported Django versions
=========================

Tested with: 

* Django 1.2.7 on python2.7
* Django 1.3.7 on python2.7
* Django 1.4.16 on python2.7
* Django 1.5.11 on python2.7, python3.2, python3.3, python3.4
* Django 1.6.8 on python2.7, python3.2, python3.3, python3.4
* Django 1.7.1 on python2.7, python3.2, python3.3, python3.4

Documentation
=============

http://kidosoft.pl/docs/django-redisdb/