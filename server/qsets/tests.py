import logging

from django.core.cache import caches
from django.test import TestCase

from .team_stats import TeamStats

logger = logging.getLogger(__name__)


class CacheTest(TestCase):
    """Common tests for types of cache invalidation"""

    def setUp(self):
        self.team_stats = TeamStats()
        logger.info("Using cache %s", type(caches['default']).__name__)
        logger.info("Adding a set of team stats, expects multiple cache invalidation")
        self.team_stats.add(name="Alpha", score=50)
        self.team_stats.add(name="Beta", score=40)
        self.team_stats.add(name="Gamma", score=10)
        self.team_stats.add(name="Delta", score=30)
        self.team_stats.add(name="Epsilon", score=20)

    def verify_top(self, expected, count=3):
        c = 0
        for team in self.team_stats.top(count):
            self.assertEqual(team.score, expected[c])
            logger.info("(%s) %s %d == %d", team.id, team.name, team.score, expected[c])
            c += 1

    def test(self):
        """
        NOTE: Cache hits/misses are logged for manual validation from the TeamStats cache
        Here we are validating only expected team stats list values are returned
        """
        logger.info("For first top team stats fetch, expects cache miss")
        self.verify_top([50, 40, 30], 3)
        logger.info("For repeated same fetch count, expects cache hit")
        self.verify_top([50, 40, 30], 3)

        logger.info("Changing top team stats fetch count to lower count, expects cache hit")
        self.verify_top([50, 40], 2)
        logger.info("For same top teams fetch count, expects cache hit")
        self.verify_top([50, 40], 2)

        logger.info("Changing top teams fetch count to higher count, expects cache invalidation")
        self.verify_top([50, 40, 30, 20], 4)
        logger.info("For same top teams fetch count, expects cache hit")
        self.verify_top([50, 40, 30, 20], 4)

        logger.info("Adding a new team stat, expects cache invalidation")
        self.team_stats.add(name="Zeta", score=60)
        self.verify_top([60, 50, 40], 3)
        logger.info("For repeated same fetch count, expects cache hit")
        self.verify_top([60, 50, 40], 3)

        logger.info("Removing a team stat, expects cache invalidation")
        self.team_stats.remove(1)
        self.verify_top([60, 40, 30], 3)
        logger.info("For repeated same fetch count, expects cache hit")
        self.verify_top([60, 40, 30], 3)
