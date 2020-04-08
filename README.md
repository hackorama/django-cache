# Django QuerySet Caching with uWSGI

> Work in progress ...

Three versions implemented.

**1. [Simple Caching](server/qsets/simple_caching.py) for a specific model only**

A simple database QuerySets caching example for only a specific Model object.
Multiple models with same id cannot be supported in the same cache because of key clash.

**2. [Generic Caching](server/qsets/generic_caching.py) for all models**

A generic database QuerySets caching example for any Model objects.
Multiple models with same id is supported in the same cache using class name prefixing to the key.

**3. [Cacheable Model Caching](server/qsets/cacheablemodel_caching.py) for all models**

Caching example using the custom [CacheableModel](server/qsets/cacheablemodel.py) class which implements generic
caching by extending Django [Model](https://docs.djangoproject.com/en/3.0/ref/models/instances/#django.db.models.Model)
class.

**Compare the versions**

| Type | Get | Set | Remove | Model |
| --- | --- | --- | --- | --- |
| Simple | `get_user(id)` | `set_user(id, "field")` | `remove_user(id)` | `User(models.Model)`  |
| Generic | `get(User, id)` | `set(id, user)` | `remove(User, id)` | `User(models.Model)`  |
|  | `get(Team, id)` | `set(id, team)` | `remove(Team, id)` | `Team(models.Model)`  |
| Cacheable Model| `User().get(id)` | `User().set(id, user)` | `User().remove(id)` | `User(CacheableModel)`  |
|  | `Team().get(id)` | `Team().set(id, team)` | `Team().remove(id)` | `Team(CacheableModel)`  |

> NOTE: [Model Signals](https://docs.djangoproject.com/en/3.0/ref/signals/) could potentially be leveraged to
> invalidate the cache behind the scenes for updates. But the above approach provides consistent interface with clear
> intention.

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
$ uwsgi --cache2 name=qsets,items=100  --http :8000 --module server.wsgi
*** Starting uWSGI 2.0.18 (64bit) on [Mon Apr  6 19:01:28 2020] ***
...
uWSGI http bound on :8000 fd 4
...
```

Trigger test

```shell script
$ curl http://127.0.0.1:8000/
```

Check server logs

```shell script
$ uwsgi --cache2 name=qsets,items=100  --http :8000 --module server.wsgi
...
uWSGI http bound on :8000 fd 5
...
Testing Django Model object specific simple caching version using UWSGICache ...
...
...
Second get of updated user with id=1
  Cache HIT key=1
Got User id=1 mame=Jane
...
...
Testing generic caching version for all Django Model objects using UWSGICache ...
...
...
First get of user with id=1
  CACHE MISS key=User.1
  CACHE POPULATE key=User.1
Got User id=1 mame=Alice
...
...
Testing new CacheableModel class version of Django Model objects using UWSGICache ...

Creating a team with id=1
  CACHE INVALIDATE key=Team.1
First get of team  with id=1
  CACHE MISS key=Team.1
  CACHE POPULATE key=Team.1
Got Team id=1 mame=Dev
Second get of team with id=1
  CACHE HIT key=Team.1
Got Team id=1 mame=Dev
Updating team with id=1
  CACHE INVALIDATE key=Team.1
First get of updated team with id=1
  CACHE MISS key=Team.1
  CACHE POPULATE key=Team.1
Got Team id=1 mame=Ops
Second get of updated team with id=1
  CACHE HIT key=Team.1
Got Team id=1 mame=Ops
Removing team with id=1
  CACHE INVALIDATE key=Team.1
Get removed team with id=1
  CACHE MISS key=Team.1
Got None

```

## Run without uWSGI

By default Django uses the built in LocMemCache when not running with uWSGI.

```shell script
$ python manage.py runserver
...
Starting development server at http://127.0.0.1:8000/
...
Testing Django Model object specific simple caching version using LocMemCache ...
...
...
Testing generic caching version for all Django Model objects using LocMemCache ...
...
...
Testing new CacheableModel class version of Django Model objects using LocMemCache ...
...
...
First get of updated team with id=1
  CACHE MISS key=Team.1
  CACHE POPULATE key=Team.1
Got Team id=1 mame=Ops
...
...
```

## Key configurations

Install uWSGI and [django-uwsgi-cache](https://pypi.org/project/django-uwsgi-cache/) using
[requirements.txt](requirements.txt)

```shell script
$ vi server/settings.py 
...
CACHES = { 
    'default': {
        'BACKEND': 'uwsgicache.UWSGICache',
        'LOCATION': 'qsets'
    }   
}  
...
```

```shell script
$ uwsgi --cache2 name=qsets,items=100  --http :8000 --module server.wsgi
```

```shell script
...
from django.core.cache import cache
from django.core.cache import caches
...
logger.info("Using cache type %s", type(caches['default']).__name__)
...
cache.get(id)
...
cache.set(id, model)
...
cache.delete(id) 
```

## TODO

- Look at [Model Signals](https://docs.djangoproject.com/en/3.0/ref/signals/) for invalidating cache for writes.
- Verify TTL timeout eviction of cache objects
- More testing of corner cases, thread safety issues etc.
- Code quality cleanup - pylint, docstrings, type hints etc.
