#!/bin/bash

# Init db and collect static files
if [[ "$MULTI_TENANT_ENABLE" == "True" ]]; then
	purplship migrate_schemas --shared || exit
else
	purplship migrate || exit
fi
purplship collectstatic --clear --noinput || exit

# Start services
set -m # turn on bash's job control

gunicorn --config gunicorn-cfg.py purpleserver.wsgi &

purplship run_huey -w 2  || exit

pkill -f gunicorn
