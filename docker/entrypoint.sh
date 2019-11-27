#!/bin/sh

cd /usr/src/openhim-mediator-multitenant/mediator/

# Register the mediator with OpenHIM
python manage.py register

# Append this scripts parameters to any Gunicorn settings specified
# using its environment variable.
GUNICORN_CMD_ARGS="$GUNICORN_CMD_ARGS $@" /usr/local/bin/gunicorn mediator.wsgi:application
