#!/bin/bash

# Setup DB and static files
purplship migrate || exit
purplship collectstatic --clear --noinput || exit

# Setup Default super admin
(echo "
from django.contrib.auth import get_user_model
if not any(get_user_model().objects.all()):
   get_user_model().objects.create_superuser('$ADMIN_EMAIL', '$ADMIN_PASSWORD')
" | purplship shell) || exit

# Start services
set -e # turn on bash's job control
trap 'kill 0' INT

gunicorn --config gunicorn-cfg.py purpleserver.asgi -k uvicorn.workers.UvicornWorker &
purplship run_huey -w $BACKGROUND_WORKERS &

wait -n
