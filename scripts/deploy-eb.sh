#!/bin/bash

VERSION=`date +%Y.%m.%d.%H.%M.%S`

while [[ $# -gt 0 ]]
do
    key="$1"

    case $key in
        -i|--build-image)
        # Build Docker image, tag and push
        scripts/build-image.sh
        shift
        ;;
        -a|--build-artifact)
        # Build Elastic Beanstalk artifact
        scripts/build-eb-artifact.sh
        shift
        ;;
    esac
done

eb deploy --label=v.$VERSION --staged
