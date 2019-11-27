#!/bin/bash
#
# Builds dimagi/openhim-mediator-multitenant:latest and pushes to Docker Hub.
#
git archive --output=git-archive.tar.gz \
    --prefix=openhim-mediator-multitenant/ \
    HEAD
docker build --tag=openhim-mediator-multitenant .
docker tag openhim-mediator-multitenant dimagi/openhim-mediator-multitenant:latest
docker push dimagi/openhim-mediator-multitenant:latest
rm -f git-archive.tar.gz
