# PurplShip (Multi-carrier private cloud shipping API)

## Introduction

purplship-server is a private cloud Multi-carrier Shipping API.


## Documentation

PurplShip has usage and reference documentation at [docs.purplship.com](https://docs.purplship.com).


## Try out PurplShip

### Docker

- Docker Image

```shell script
docker run \
  -p80:8000 \
  --name=pship --rm \
  --volume=$(pwd):/app \
  --interactive --tty purplship/purplship-server:2020.6.1 \
  /bin/bash -c "purplship makemigrations && purplship migrate && purplship createsuperuser ; purplship runserver 0.0.0.0:8000"
```

- Docker Compose

create a configuration file

```shell script
echo > docker-compose.yml
```

paste this configuration
```yaml
version: '3'

services:
  db:
    image: postgres
    restart: always
    environment:
      POSTGRES_DB: "db"
      POSTGRES_USER: "postgres"
      POSTGRES_PASSWORD: "postgres"
  web:
    image: purplship/purplship-server:2020.6.1
    restart: always
    entrypoint: |
      bash -c "bash -s <<EOF
      purplship makemigrations &&
      purplship migrate &&
      (echo \"from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'demo')\" | purplship shell) > /dev/null 2>&1;
      purplship runserver 0.0.0.0:8000
      EOF"
    environment:
      - DEBUG_MODE=True
      - ALLOWED_HOSTS=*
      - DATABASE_HOST=db
      - DATABASE_PORT=5432
      - DATABASE_NAME=db
      - DATABASE_ENGINE=postgresql_psycopg2
      - DATABASE_USERNAME=postgres
      - DATABASE_PASSWORD=postgres
    volumes:
      - .:/app
    ports:
      - "80:8000"
    depends_on:
      - db
```

```shell script
docker-compose up
```


### Using Pip (For development)

- OS Requirements

Python >= 3.7 

- Install

create a python virtual environment using [python venv](https://docs.python.org/3/tutorial/venv.html)

```shell script
pip install -f https://git.io/purplship purplship-server==2020.6.1
```

**For the latest stable installation with frozen version**

<details>
<summary>Installation from dependencies lock</summary>

copy this in a `requirement.txt` file

```text
-f https://git.io/purplship
asgiref==3.2.7
attrs==19.3.0
certifi==2020.4.5.1
chardet==3.0.4
coreapi==2.3.3
coreschema==0.0.4
Django==3.0.7
djangorestframework==3.11.0
djangorestframework-camel-case==1.1.2
drf-yasg==1.17.1
idna==2.9
inflection==0.4.0
itypes==1.2.0
Jinja2==2.11.2
jstruct==2020.4.0
lxml==4.5.1
MarkupSafe==1.1.1
packaging==20.4
purplship==2020.6.1
purplship.package==2020.6.1
purplship.canadapost==2020.6.1
purplship.dhl==2020.6.1
purplship.fedex==2020.6.1
purplship.purolator==2020.6.1
purplship.ups==2020.6.1
py-canadapost==2020.4.0
py-dhl==2020.4.0
py-fedex==2020.3.0
py-purolator==2020.4.0
py-soap==2020.3.0
py-ups==2020.3.0
pyparsing==2.4.7
pytz==2020.1
requests==2.23.0
ruamel.yaml==0.16.10
ruamel.yaml.clib==0.2.0
six==1.15.0
sqlparse==0.3.1
uritemplate==3.0.1
urllib3==1.25.9
xmltodict==0.12.0
```

```shell script
pip install -r requirement.txt
```
</details>


- Initialize database (Demo)

```shell script
purplship makemigrations
purplship migrate
purplship createsuperuser
# Enter your credentials in the prompt
```

- Start the server (Demo)

```shell script
purplship runserver 0.0.0.0:8000
```
