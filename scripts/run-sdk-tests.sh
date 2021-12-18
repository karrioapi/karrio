#!/usr/bin/env bash

source "scripts/activate-env.sh"

if [[ "$*" != *--insiders* ]];
then
    nosetests -x -v --with-coverage $(find sdk -type d -name "tests")
else
    nosetests -x -v --with-coverage $(find sdk insiders/sdk -type d -name "tests")
fi
