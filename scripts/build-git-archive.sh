#!/bin/sh

git archive --output=git-archive.tar \
    --prefix=openhim-mediator-passthrough/ \
    HEAD

cd submodules/openhim-mediator-utils-py/
git archive --output=../../git-archive-submodule.tar \
    --prefix=openhim-mediator-passthrough/submodules/openhim-mediator-utils-py/ \
    HEAD

cd ../..
tar -Af git-archive.tar git-archive-submodule.tar
rm git-archive-submodule.tar
gzip git-archive.tar
