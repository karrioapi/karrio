#!/usr/bin/env bash

test() {
    python -m unittest -v
}

typecheck() {
    mypy purplship/ --no-strict-optional --no-warn-return-any --no-warn-unused-configs
}

check() {
    typecheck && test 
}

build() {
    python setup.core.py bdist_wheel
    python setup.freight.py bdist_wheel
    python setup.shipping.py bdist_wheel
}

updaterelease(){
    git tag -f -a $1
    git push -f --tags
}
