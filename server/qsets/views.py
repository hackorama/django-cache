import logging

from django.core.cache import cache
from django.core.cache import caches
from django.http import HttpResponse

from .models import User

logger = logging.getLogger(__name__)


def index(request):
    logger.info("Using cache type %s", caches['default'])
    logger.info("Creating a user ...")
    set_user('1', "foo")
    logger.info("First get of user")
    user = get_user('1')
    logger.info(user)
    logger.info("Second get of user")
    user = get_user('1')
    logger.info(user)
    logger.info("Updating user name ...")
    set_user('1', "bar")
    logger.info("First get of updated user")
    user = get_user('1')
    logger.info(user)
    logger.info("Next get of updated user")
    user = get_user('1')
    logger.info(user)
    logger.info("Deleting user ...")
    remove_user('1')

    return HttpResponse("Testing QuerySet Caching")


def get_user(id):
    user = cache.get(id)
    if user is None:  # Not in cache
        logger.info("Cache miss %s", id)
        user = User.objects.filter(id=id)
        if user is not None:  # Found in DB
            logger.info("Cache add %s", id)
            cache.set(id, user)  # Add to cache
    else:
        logger.info("Cache hit %s", id)
    return user


def set_user(id, name):
    # TODO: Use post_save model signal to invalidate ?
    logger.info("Cache invalidate %s", id)
    cache.delete(id)  # Invalidate from cache
    User.objects.update_or_create(id=id, defaults={'id': id, 'name': name})


def remove_user(id):
    # TODO: Use model signal to invalidate ?
    logger.info("Cache invalidate %s", id)
    cache.delete(id)  # Invalidate from cache
    User.objects.filter(id=id).delete()
    pass
