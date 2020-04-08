"""
Caching example using the custom CacheableModel class which implements generic caching by extending Django Model class.
"""
import logging

from .models import Team

logger = logging.getLogger(__name__)


def test():
    id = 1
    logger.info("Creating a team with id=%s", id)
    team = Team()
    team.name = "Dev"
    Team().set(id, team)
    logger.info("First get of team  with id=%s", id)
    team = Team().get(id)
    logger.info("Got %s", team)
    logger.info("Second get of team with id=%s", id)
    team = Team().get(id)
    logger.info("Got %s", team)
    logger.info("Updating team with id=%s", id)
    team = Team()
    team.name = "Ops"
    Team().set(id, team)
    logger.info("First get of updated team with id=%s", id)
    team = Team().get(id)
    logger.info("Got %s", team)
    logger.info("Second get of updated team with id=%s", id)
    team = Team().get(id)
    logger.info("Got %s", team)
    logger.info("Removing team with id=%s", id)
    Team().remove(id)
    logger.info("Get removed team with id=%s", id)
    team = Team().get(id)
    logger.info("Got %s", team)
