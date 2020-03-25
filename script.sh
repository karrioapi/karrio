#!/usr/bin/env bash

test() {
    pushd tests
    python -m unittest -v $@
    popd
}

typecheck() {
    mypy purplship/ --no-strict-optional --no-warn-return-any --no-warn-unused-configs
}

check() {
    typecheck && test 
}

build_package() {
    clean_builds
    python setup.package.py bdist_wheel
}

build_freight() {
    clean_builds
    python setup.freight.py bdist_wheel
}

build() {
    clean_builds
    python setup.py bdist_wheel
}

updaterelease(){
    git tag -f -a $1
    git push -f --tags
}

clean_builds() {
    find . -type d -name dist -exec rm -r {} \;
    find . -type d -name build -exec rm -r {} \;
    find . -type d -name *.egg-info -exec rm -r {} \;
}
