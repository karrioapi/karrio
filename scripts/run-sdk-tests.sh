#!/usr/bin/env bash

source "scripts/activate-env.sh"

nosetests -x -v --with-coverage $(find sdk insiders/sdk -type d -name "tests")
