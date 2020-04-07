# Django QuerySet Caching with uWSGI

> Work in progress with a very basic version ...

## Quick Start

```shell script
$ python -m venv venv
$ source venv/bin/activate
$ python -m pip install -r requirements.txt
$ cd server
$ python manage.py migrate
```

## Run using uWSGI 

```shell script
$ uwsgi --http :8000 --module server.wsgi
*** Starting uWSGI 2.0.18 (64bit) on [Mon Apr  6 19:01:28 2020] ***
...

Starting development server at http://127.0.0.1:8000/
...
uWSGI http bound on :8000 fd 4
...
```

```shell script
$ curl  http://127.0.0.1:8000/
```

```shell script
Using cache type <uwsgicache.UWSGICache object at 0x10e7dda50>
Creating a user ...
Cache invalidate 1
First get of user
Cache miss 1
Cache add 1
<QuerySet [<User: foo>]>
Second get of user
Cache miss 1
Cache add 1
<QuerySet [<User: foo>]>
Updating user name ...
Cache invalidate 1
First get of updated user
Cache miss 1
Cache add 1
<QuerySet [<User: bar>]>
Next get of updated user
Cache miss 1
Cache add 1
<QuerySet [<User: bar>]>
Deleting user ...
Cache invalidate 1


```

## Run without uWSGI

By default Django uses the built in LocMemCache when not running with uWSGI.

```shell script
$ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
...
Using cache type <django.core.cache.backends.locmem.LocMemCache object at 0x10b6c20d0>
Creating a user ...
Cache invalidate 1
First get of user
Cache miss 1
Cache add 1
<QuerySet [<User: foo>]>
Second get of user
Cache hit 1
<QuerySet [<User: foo>]>
Updating user name ...
Cache invalidate 1
First get of updated user
Cache miss 1
Cache add 1
<QuerySet [<User: bar>]>
Next get of updated user
Cache hit 1
<QuerySet [<User: bar>]>
Deleting user ...
Cache invalidate 1
```

## Key configuration

Install uWSGI and [django-uwsgi-cache](https://pypi.org/project/django-uwsgi-cache/)
(Installed from [requiremnets.txt](requirements.txt))

```shell script
$ vi server/settings.py 
...
CACHES = { 
    'default': {
        'BACKEND': 'uwsgicache.UWSGICache',
    }   
}  
...
```

```shell script
$ vi server/qsets/views.py 
...
from django.core.cache import cache
from django.core.cache import caches
...
logger.info("Using cache type %s", caches['default'])
...
user = cache.get(id)
...
cache.set(id, user)
...
cache.delete(id) 
```

## TODO

- Look at [Model Signals](https://docs.djangoproject.com/en/3.0/ref/signals/) for invalidating cache for writes.
- Set TTL for cache objects ?
