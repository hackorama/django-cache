"""
A generic database QuerySets caching example for any Model objects.
Multiple models with same id is supported in the same cache using class name prefixing to the key.
"""
import logging

from django.core.cache import cache

from .models import User

logger = logging.getLogger(__name__)


def test():
    id = 1
    logger.info("Creating a user with id=%s", id)
    user = User()
    user.name = "Alice"
    set(id, user)
    logger.info("First get of user with id=%s", id)
    user = get(User, id)
    logger.info("Got %s", user)
    logger.info("Second get of user with id=%s", id)
    user = get(User, id)
    logger.info("Got %s", user)
    logger.info("Updating user with id=%s", id)
    user = User()
    user.name = "Bob"
    set(id, user)
    logger.info("First get of updated user with id=%s", id)
    user = get(User, id)
    logger.info("Got %s", user)
    logger.info("Second get of updated user with id=%s", id)
    user = get(User, id)
    logger.info("Got %s", user)
    logger.info("Removing user with id=%s", id)
    remove(User, id)
    logger.info("Get removed user with id=%s", id)
    user = get(User, id)
    logger.info("Got %s", user)


def build_key(model, id):
    """
    Build cache key combining model class name and id
    :param model:  the model class came
    :param id: the primary key id
    :return: the key as <name>.<id>
    """
    return "{}.{}".format(model.__name__, id)


def get(model_class, id):
    """
    Get a model object from the cache.
    If the object is not in cache gets it from the database and also populates it in the cache.

    :param model_class: the model class
    :param id: the primary key of the model
    :return: the model object or None
    """
    key = build_key(model_class, id)
    user = cache.get(key)
    if user is None:  # Not in cache
        logger.info("  CACHE MISS key=%s", key)
        user = User.objects.filter(id=id).first()
        if user is not None:  # Found in DB
            logger.info("  CACHE POPULATE key=%s", key)
            cache.set(key, user)  # Add to cache
    else:
        logger.info("  CACHE HIT key=%s", key)
    return user


def set(id, model):
    """
    Creates or updates given model object into database with the given primary key id
    and invalidates any cached version.

    NOTE: The model class name is found from the model object.

    :param id: the primary key of the model to create or update
    :param model: the model to create or update
    :return: None
    """
    key = build_key(type(model), id)  # Get model class from model object
    logger.info("  CACHE INVALIDATE key=%s", key)
    cache.delete(key)  # Invalidate from cache
    model.id = id
    model.save()


def remove(model_class, id):
    """
    Removes model object from the database and invalidates any cached version.

    :param model_class: the model class
    :param id: the primary key of the model
    :return: None
    """
    key = build_key(model_class, id)
    logger.info("  CACHE INVALIDATE key=%s", key)
    cache.delete(key)  # Invalidate from cache
    User.objects.filter(id=id).delete()
