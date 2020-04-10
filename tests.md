# QuerySet Caching Tests

An example of caching a set of models from an expensive query lookup by caching the QuerySet.

Added [TeamStats](server/qsets/team_stats.py) that implements top n `TeamStat` lookup.

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


Tested with new [CacheTest](server/qsets/tests.py)

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
For first top 3 team stats fetch, expects cache miss
Getting top 3 team stats
  CACHE MISS
  CACHE POPULATE
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
For repeated same etch count of 3, expects cache hit
Getting top 3 team stats
  CACHE HIT
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30

Changing top team stats fetch count to lower count of 2, expects cache hit
Getting top 2 team stats
  CACHE HIT FOR SUBSET [IN CACHE 3, REQUESTED 2]
(1) Alpha 50 == 50
(2) Beta 40 == 40
For same top teams fetch count of 2, expects cache hit
Getting top 2 team stats
  CACHE HIT FOR SUBSET [IN CACHE 3, REQUESTED 2]
(1) Alpha 50 == 50
(2) Beta 40 == 40

Changing top teams fetch count to higher count of 4, expects cache invalidation
Getting top 4 team stats
  CACHE MISS [IN CACHE 3, REQUESTED 4]
  CACHE INVALIDATE
  CACHE POPULATE
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
(5) Epsilon 20 == 20
For same top teams fetch count of 4, expects cache hit
Getting top 4 team stats
  CACHE HIT
(1) Alpha 50 == 50
(2) Beta 40 == 40
(4) Delta 30 == 30
(5) Epsilon 20 == 20

Adding a new team stat and fetching 3, expects cache invalidation
  CACHE INVALIDATE
Getting top 3 team stats
  CACHE MISS
  CACHE POPULATE
(6) Zeta 60 == 60
(1) Alpha 50 == 50
(2) Beta 40 == 40
For repeated same fetch count of 3, expects cache hit
Getting top 3 team stats
  CACHE HIT
(6) Zeta 60 == 60
(1) Alpha 50 == 50
(2) Beta 40 == 40

Removing a team stat and fetching 3, expects cache invalidation
  CACHE INVALIDATE
Getting top 3 team stats
  CACHE MISS
  CACHE POPULATE
(6) Zeta 60 == 60
(2) Beta 40 == 40
(4) Delta 30 == 30
For repeated same fetch count of 3, expects cache hit
Getting top 3 team stats
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

