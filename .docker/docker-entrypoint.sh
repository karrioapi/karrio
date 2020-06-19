#!/bin/bash

# Init db, collect and collect statics
purplship makemigrations &&
purplship migrate &&
purplship collectstatic --noinput &&
(echo "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USERNAME}', 'admin@example.com', '${ADMIN_PASSWORD}')" | purplship shell) > /dev/null 2>&1;
purplship runserver "0.0.0.0:$PURPLSHIP_PORT"
