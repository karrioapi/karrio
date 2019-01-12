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
    python setup.py bdist_wheel 
}
