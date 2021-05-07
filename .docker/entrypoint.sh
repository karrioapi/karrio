#!/bin/bash

# Init db and collect static files
if [[ "$MULTI_TENANT_ENABLE" == "True" ]]; then
	purplship migrate_schemas --shared || exit
else
	purplship migrate || exit
fi
purplship collectstatic --clear --noinput || exit

if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
then
	(echo "
from purpleserver.tenants.models import Client, Domain
if not any(Client.objects.all()):
  Domain.objects.create(domain='admin.purplship.com', tenant=Client.objects.create(name='public', schema_name='public'))
  Domain.objects.create(domain='app.purplship.com', tenant=Client.objects.create(name='purplship', schema_name='purplship'))
" | purplship shell) > /dev/null 2>&1;

    (echo "
from django_tenants.utils import tenant_context
from django.contrib.auth import get_user_model
from purpleserver.tenants.models import Client
with tenant_context(Client.objects.get(schema_name='public')):
  if not any(get_user_model().objects.all()):
     get_user_model().objects.create_superuser('${TENANT_ADMIN_EMAIL}', '${TENANT_ADMIN_PASSWORD}')
with tenant_context(Client.objects.get(schema_name='purplship')):
  if not any(get_user_model().objects.all()):
     get_user_model().objects.create_superuser('${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
" | purplship shell) > /dev/null 2>&1;

else
  (echo "
from purpleserver.user.models import User;
if not any(User.objects.all()):
  User.objects.create_superuser('${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
" | purplship shell) > /dev/null 2>&1;
fi


set -m # turn on bash's job control

gunicorn --config gunicorn-cfg.py purpleserver.wsgi &

purplship run_huey -w 2  || exit

pkill -f gunicorn
