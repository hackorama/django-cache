import logging

from django.core.cache import cache
from django.db import models

logger = logging.getLogger(__name__)


class CacheableModel(models.Model):
    """A cache enabled version of Model"""

    def build_key(self, id):
        """
        Build cache key combining model class name and id
        :param id: the primary key id
        :return: the key as <class_name>.<id>
        """
        return "{}.{}".format(self.__class__.__name__, id)

    def get(self, id):

        """
        Get a model object from the cache.
        If the object is not in cache gets it from the database and also populates it in the cache.

        :param id: the primary key of the model
        :return: the model object or None
        """
        key = self.build_key(id)
        model = cache.get(key)
        if model is None:  # Not in cache
            logger.info("  CACHE MISS key=%s", key)
            model = self.__class__.objects.filter(id=id).first()
            if model is not None:  # Found in DB
                logger.info("  CACHE POPULATE key=%s", key)
                cache.set(key, model)  # Add to cache
        else:
            logger.info("  CACHE HIT key=%s", key)
        return model

    def set(self, id, model):
        """
        Creates or updates given model object into database with the given primary key id
        and invalidates any cached version.

        :param id: the primary key of the model to create or update
        :param model: the model to create or update
        :return: None
        """
        key = self.build_key(id)  # Get model class from model object
        logger.info("  CACHE INVALIDATE key=%s", key)
        cache.delete(key)  # Invalidate from cache
        model.id = id
        model.save()

    def remove(self, id):
        """
        Removes model object from the database and invalidates any cached version.

        :param model_class: the model class
        :param id: the primary key of the model
        :return: None
        """
        key = self.build_key(id)
        logger.info("  CACHE INVALIDATE key=%s", key)
        cache.delete(key)  # Invalidate from cache
        self.__class__.objects.filter(id=id).delete()
