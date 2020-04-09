# Tests


## Added [TeamStats](server/qsets/team_stats.py) 

Get the top team stats of given count by team score with QuerySet caching

- QuerySet is cached as a list of models
- Invalidation is based on change in model item count
- Any add/delete of a model causes a cache invalidation
- For the first top items fetch count - cache miss
- For the same top items fetch count - cache hit
- For top items fetch count more than already cached - cache miss
- For top items fetch count less than already cached - cache hit (subset of cached list)

> NOTE: Cache operations are logged out for validation from test runs

> [Model Signals](https://docs.djangoproject.com/en/3.0/ref/signals/) could potentially be leveraged to
> invalidate the cache behind the scenes for updates

## Added [CacheTest](server/qsets/tests.py)


```
$ python -m pip install -r requirements.txt
$ cd server
$ python manage.py migrate
```

```
$ python manage.py test qsets.tests
Creating test database for alias 'default'...
...
Using cache LocMemCache
...
For first top team stats fetch, expects cache miss
  CACHE MISS
  CACHE POPULATE
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
For repeated same fetch count, expects cache hit
  CACHE HIT
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30

Changing top team stats fetch count to lower count, expects cache hit
  CACHE HIT FOR SUBSET [IN CACHE 3, REQUESTED 2]
(1) Alpha 50 == 50
(2) Beta 40 == 40
For same top teams fetch count, expects cache hit
  CACHE HIT FOR SUBSET [IN CACHE 3, REQUESTED 2]
(1) Alpha 50 == 50
(2) Beta 40 == 40

Changing top teams fetch count to higher count, expects cache invalidation
  CACHE MISS [IN CACHE 3, REQUESTED 4]
  CACHE INVALIDATE
  CACHE POPULATE
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
(5) Epsilon 20 == 20

For same top teams fetch count, expects cache hit
  CACHE HIT
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
(5) Epsilon 20 == 20

Adding a new team stat, expects cache invalidation
  CACHE INVALIDATE
  CACHE MISS
  CACHE POPULATE
(6) Zeta 60 == 60
(1) Alpha 50 == 50
(2) Beta 40 == 40
For repeated same fetch count, expects cache hit
  CACHE HIT
(6) Zeta 60 == 60
(1) Alpha 50 == 50
(2) Beta 40 == 40

Removing a team stat, expects cache invalidation
  CACHE INVALIDATE
  CACHE MISS
  CACHE POPULATE
(6) Zeta 60 == 60
(2) Beta 40 == 40
(4) Delta 30 == 30
For repeated same fetch count, expects cache hit
  CACHE HIT
(6) Zeta 60 == 60
(2) Beta 40 == 40
(4) Delta 30 == 30
.
----------------------------------------------------------------------
Ran 1 test in 0.009s

OK
Destroying test database for alias 'default'...
```

