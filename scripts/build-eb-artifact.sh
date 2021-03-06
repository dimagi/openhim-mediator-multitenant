#!/bin/sh

# Creates an AWS Elastic Beanstalk artifact for deployment
#


if [ -z "$ENVIRONMENT_NAME" ]
then
    echo Environment variables have not been set. Use
    echo "    \$ source env/<target environment name>"
    exit 1
fi

echo Building AWS Elastic Beanstalk artifact for $ENVIRONMENT_NAME environment

rm -f eb-artifact.zip

# Add git archive to artifact
git archive --format=zip HEAD > eb-artifact.zip

# Render config files for production
scripts/render-env.py docker/templates/mediator.conf > docker/nginx/conf.d/mediator.conf
scripts/render-env.py docker/templates/Dockerrun.aws.json > Dockerrun.aws.json

# Add files excluded by git archive
python mediator/manage.py collectstatic --noinput
cp submodules/docker-nginx-certbot/src/nginx_conf.d/*.conf docker/nginx/conf.d/
zip -r eb-artifact.zip mediator/mediator/static
zip eb-artifact.zip docker/nginx/conf.d/*.conf
zip eb-artifact.zip Dockerrun.aws.json

# Clean up
rm docker/nginx/conf.d/*.conf
