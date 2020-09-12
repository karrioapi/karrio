#!/bin/bash

# Init db and collect static files
purplship makemigrations &&
if [[ "$MULTI_TENANT_ENABLE" == "True" ]]; then purplship migrate_schemas; else purplship migrate; fi &&
purplship collectstatic --noinput ||
exit

if [[ "$MULTI_TENANT_ENABLE" == "True" ]];
then
  (echo "from purpleserver.tenants.models import Client; Client.objects.create(name='public', schema_name='public', domain_url='console.purpleserver.local')" | purplship shell) > /dev/null 2>&1;
  (echo "from django.contrib.auth.models import User; User.objects.create_superuser('root', 'root@example.com', '${ADMIN_PASSWORD}')" | purplship shell) > /dev/null 2>&1;

  (echo "from purpleserver.tenants.models import Client; Client.objects.create(name='general', schema_name='general', domain_url='app.purpleserver.local')" | purplship shell) > /dev/null 2>&1;
  (echo "from tenant_schemas.utils import tenant_context; from django.contrib.auth.models import User; from purpleserver.tenants.models import Client;
with tenant_context(Client.objects.get(schema_name='general')):
  User.objects.create_superuser('${ADMIN_USERNAME}', 'admin@example.com', '${ADMIN_PASSWORD}')" | purplship shell) > /dev/null 2>&1;
else
  (echo "from django.contrib.auth.models import User; User.objects.create_superuser('${ADMIN_USERNAME}', 'admin@example.com', '${ADMIN_PASSWORD}')" | purplship shell) > /dev/null 2>&1;
fi

gunicorn --chdir /usr/local/lib/python3.8/site-packages/ --config gunicorn-cfg.py purpleserver.wsgi
