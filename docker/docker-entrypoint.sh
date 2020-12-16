#!/bin/bash

# Init db and collect static files
purplship makemigrations &&
if [[ "$MULTI_TENANT_ENABLE" == "True" ]]; then purplship migrate_schemas; else purplship migrate; fi &&
purplship collectstatic --noinput ||
exit

if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
then
  (echo "
from purpleserver.tenants.models import Client
if not any(Client.objects.all()):
  Client.objects.create(name='public', schema_name='public', domain_url='console.purpleserver.com')
" | purplship shell) > /dev/null 2>&1;

  (echo "
from purpleserver.user.models import User
if not any(User.objects.all()):
   User.objects.create_superuser('${TENANT_ADMIN_EMAIL}', '${TENANT_ADMIN_PASSWORD}')
" | purplship shell) > /dev/null 2>&1;

  (echo "
from purpleserver.tenants.models import Client
if not any(Client.objects.all()):
  Client.objects.create(name='general', schema_name='general', domain_url='app.purpleserver.com')
" | purplship shell) > /dev/null 2>&1;

  (echo "
from tenant_schemas.utils import tenant_context; from purpleserver.user.models import User; from purpleserver.tenants.models import Client;
with tenant_context(Client.objects.get(schema_name='general')):
  if not any(User.objects.all()):
    User.objects.create_superuser('${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
" | purplship shell) > /dev/null 2>&1;

else
  (echo "
from purpleserver.user.models import User;
if not any(User.objects.all()):
  User.objects.create_superuser('${ADMIN_EMAIL}', '${ADMIN_PASSWORD}')
" | purplship shell) > /dev/null 2>&1;
fi

gunicorn --chdir /usr/local/lib/python3.8/site-packages/ --config gunicorn-cfg.py purpleserver.wsgi
