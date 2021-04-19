#!/bin/bash

set -m # turn on bash's job control

gunicorn --chdir /usr/local/lib/python3.8/site-packages/ --config gunicorn-cfg.py purpleserver.wsgi &

purplship run_huey -w 2 &

fg %1
