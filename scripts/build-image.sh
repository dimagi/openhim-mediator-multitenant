#!/bin/bash
#
# Builds dimagi/openhim-mediator-passthrough:latest and pushes to Docker Hub.
#
scripts/build-git-archive.sh
docker build --tag=openhim-mediator-passthrough .
docker tag openhim-mediator-passthrough dimagi/openhim-mediator-passthrough:latest
docker push dimagi/openhim-mediator-passthrough:latest
rm -f git-archive.tar.gz
