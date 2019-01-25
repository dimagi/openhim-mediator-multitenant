#!/bin/bash

# Creates an AWS Elastic Beanstalk artifact for deployment
#

rm -f eb-artifact.zip

# Add git archive to artifact
git archive --format=zip HEAD > eb-artifact.zip

# Render config files for production
ORIGINAL_PYTHONPATH="$PYTHONPATH"
ORIGINAL_SETTINGS_MODULE="$DJANGO_SETTINGS_MODULE"
export PYTHONPATH="$(pwd)/mediator"
export DJANGO_SETTINGS_MODULE="mediator.settings.production"
scripts/render-env.py docker/templates/mediator.conf > docker/nginx/conf.d/mediator.conf
scripts/render-env.py docker/templates/Dockerrun.aws.json > Dockerrun.aws.json
export PYTHONPATH="$ORIGINAL_PYTHONPATH"
export DJANGO_SETTINGS_MODULE="$ORIGINAL_SETTINGS_MODULE"

# Add files excluded by git archive
cp submodules/docker-nginx-certbot/src/nginx_conf.d/*.conf docker/nginx/conf.d/
zip eb-artifact.zip docker/nginx/conf.d/*.conf
zip eb-artifact.zip Dockerrun.aws.json

# Clean up
rm docker/nginx/conf.d/*.conf
