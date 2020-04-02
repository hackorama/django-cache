# Django QuerySet Caching with uWSGI

A demo [Django](https://www.djangoproject.com) application that uses
[uWSGI caches](https://uwsgi-docs.readthedocs.io/en/latest/Caching.html) to cache
[QuerySets](https://docs.djangoproject.com/en/3.0/ref/models/querysets/)

## Design

A demo web application using the built-in [SQLite](https://www.sqlite.org/index.html) database with data access
implemented through ORM layer using data [models](https://docs.djangoproject.com/en/3.0/topics/db/models/) and
[QuerySets](https://docs.djangoproject.com/en/3.0/ref/models/querysets/#django.db.models.query.QuerySet).

The Django application will be configured to be deployed using
[uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/WSGIquickstart.html) and [NGINX](https://www.nginx.com)
With uWSGI configured to enable caching.
The application with the servers will be packaged as a Docker image with all dependencies for quick deployment.

> TODO
