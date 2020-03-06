#!/usr/bin/env bash

build_all() {
    mkdir -p ./dist
    for d in py-*/ ; do
        cd ${d} &&
        python setup.py bdist_wheel &&
        cd ..
    done
    find . -name \*.whl -exec mv {} ./dist \;
}

clean_builds() {
    find . -type d -name dist -exec rm -r {} \;
    find . -type d -name build -exec rm -r {} \;
    find . -type d -name *.egg-info -exec rm -r {} \;
}
