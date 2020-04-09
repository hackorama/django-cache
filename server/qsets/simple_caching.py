"""
A simple database QuerySets caching example for only a specific Model object.
Multiple models with same id cannot be supported in the same cache because of key clash.
"""
import logging

from django.core.cache import cache

from .models import User

logger = logging.getLogger(__name__)


def test():
    id = 1
    logger.info("Creating user with id=%s", id)
    set_user(id, "John")
    logger.info("First get of user with id=%s", id)
    user = get_user(id)
    logger.info("Got %s", user)
    logger.info("Second get of user with id=%s", id)
    user = get_user(id)
    logger.info("Got %s", user)
    logger.info("Updating user with id=%s", id)
    set_user(id, "Jane")
    logger.info("First get of updated user with id=%s", id)
    user = get_user(id)
    logger.info("Got %s", user)
    logger.info("Second get of updated user with id=%s", id)
    user = get_user(id)
    logger.info("Got %s", user)
    logger.info("Removing user with id=%s", id)
    remove_user(id)
    logger.info("Get removed user with id=%s", id)
    user = get_user(id)
    logger.info("Got %s", user)


def get_user(id):
    user = cache.get(id)
    if user is None:  # Not in cache
        logger.info("  CACHE MISS key=%s", id)
        user = User.objects.filter(id=id).first()
        if user is not None:  # Found in DB
            logger.info("  CACHE POPULATE key=%s", id)
            cache.set(id, user)  # Add to cache
    else:
        logger.info("  CACHE HIT key=%s", id)
    return user


def set_user(id, name):
    # TODO: Use post_save model signal to invalidate ?
    logger.info("  CACHE INVALIDATE key=%s", id)
    cache.delete(id)  # Invalidate from cache
    User.objects.update_or_create(id=id, defaults={'id': id, 'name': name})


def remove_user(id):
    # TODO: Use model signal to invalidate ?
    logger.info("  CACHE INVALIDATE key=%s", id)
    cache.delete(id)  # Invalidate from cache
    User.objects.filter(id=id).delete()
