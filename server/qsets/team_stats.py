import logging

from django.core.cache import cache

from .models import TeamStat

logger = logging.getLogger(__name__)


class TeamStats:
    """
    Get the top team stats of given count by team score with QuerySet caching

    QuerySet is cached as a list of models
    Invalidation is based on change in model item count
    Any add/delete of a model causes a cache invalidation
    For the first top items fetch count - cache miss
    For the same top items fetch count - cache hit
    For top items fetch count more than already cached - cache miss
    For top items fetch count less than already cached - cache hit (subset of cached list)

    NOTE: Cache operations are logged out for validation from test runs
    TODO: Model Signals could potentially be leveraged to invalidate the cache behind the scenes for updates
    """

    CACHE_KEY = "TOP_TEAM_STATS"

    def top(self, count=3):
        """
        Get the top team stats of given count by score

        NOTE: An example of an expensive operation, whose results should be cached.

        :param count: the number of top team stats to return
        :return: list of top team stats
        """
        top = cache.get(self.CACHE_KEY)
        if not top:  # Not in cache
            logger.info("  CACHE MISS")
            top = self.__populate(count)
        elif count > len(top):
            logger.info("  CACHE MISS [IN CACHE %s, REQUESTED %s]", len(top), count)
            self.__invalidate()
            top = self.__populate(count)
        elif count < len(top):
            logger.info("  CACHE HIT FOR SUBSET [IN CACHE %s, REQUESTED %s]", len(top), count)
            top = top[:count]
        else:
            logger.info("  CACHE HIT")
        return top

    def add(self, name, score):
        """
        Add a new team stat and do cache invalidation

        NOTE: Example of cache invalidation when there is a change in model count (add)

        :param name: name of the team
        :param score:  the team score
        :return:
        """
        self.__invalidate()
        TeamStat.objects.create(name=name, score=score)

    def remove(self, id):
        """
        Remove a team stat of given id and do cache invalidation

        NOTE: Example of cache invalidation when there is a change in model count (remove)

        :param id: the id of team stat to remove
        :return:
        """
        self.__invalidate()
        TeamStat.objects.filter(id=id).delete()

    def __populate(self, count):
        """
        Populate cache with given count of team stats from database and return the top team stats

        :param count: the number of top team stats to return
        :return: list of top team stats
        """
        top = []  # Convert QuerySet to model list and cache
        # TODO Look for any optimization for the order by query (indexing)
        for teamstat in TeamStat.objects.all().order_by('-score')[:count]:
            top.append(teamstat)
        logger.info("  CACHE POPULATE")
        cache.set(self.CACHE_KEY, top)
        return top

    def __invalidate(self):
        """
        Invalidate cache

        :return: None
        """
        logger.info("  CACHE INVALIDATE")
        cache.delete(self.CACHE_KEY)
