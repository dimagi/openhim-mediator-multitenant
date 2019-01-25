#!/bin/sh

# Register the mediator with OpenHIM
/usr/local/bin/django-admin register

# Append this scripts parameters to any Gunicorn settings specified
# using its environment variable.
GUNICORN_CMD_ARGS="$GUNICORN_CMD_ARGS $@" /usr/local/bin/gunicorn mediator.wsgi:application
