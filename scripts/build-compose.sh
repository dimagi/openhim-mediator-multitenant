#!/bin/sh
#
# Builds a docker-compose.yaml file
#

if [ -z "$ENVIRONMENT_NAME" ]
then
    echo Environment variables have not been set. Use
    echo "    \$ source env/<target environment name>"
    exit 1
fi

scripts/render-env.py docker/templates/docker-compose.yaml > docker-compose.yaml
