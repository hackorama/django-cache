import logging

from django.db import models

from .cacheablemodel import CacheableModel

logger = logging.getLogger(__name__)


class User(models.Model):
    """
    This is a regular model
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return "User id={} mame={}".format(self.id, self.name)


class Team(CacheableModel):
    """
    This is a model using CachingModel a caching version of models.Model
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return "Team id={} mame={}".format(self.id, self.name)
