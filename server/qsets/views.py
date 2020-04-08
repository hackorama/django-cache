import logging
import os

from django.core.cache import caches
from django.http import HttpResponse

from . import cacheablemodel_caching
from . import generic_caching
from . import simple_caching

logger = logging.getLogger(__name__)


def index(request):
    cache = type(caches['default']).__name__
    logger.info("{}Testing Django Model object specific simple caching version using {} ...{}".format(os.linesep, cache,
                                                                                                      os.linesep))
    simple_caching.test()
    logger.info(
        "{}Testing generic caching version for all Django Model objects using {} ...{}".format(os.linesep, cache,
                                                                                               os.linesep))
    generic_caching.test()
    logger.info(
        "{}Testing new CacheableModel class version of Django Model objects using {} ...{}".format(os.linesep, cache,
                                                                                                   os.linesep))
    cacheablemodel_caching.test()
    return HttpResponse("Testing QuerySet Caching, please check the server logs{}".format(os.linesep))
