#!/bin/sh
export DJANGO_SETTINGS_MODULE='heroku.settings'

cd ./heroku

pip3 install -r requirements.txt &&
purplship migrate &&
purplship collectstatic --noinput


# Create super user for demo
(echo "
from django.contrib.auth import get_user_model
if not any(get_user_model().objects.all()):
	get_user_model().objects.create_superuser('$ADMIN_EMAIL', '$ADMIN_PASSWORD')
" | purplship shell)
