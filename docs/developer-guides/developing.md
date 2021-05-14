# Developing

- A bash compatible shell (OSX, Linux or Windows Linux subsystem)
- Docker and docker-compose

## Clone the repo

```bash
git clone git@github.com:Purplship/purplship-server.git
```

## Source the `bash` script

```bash
cd purplship-server

source ./script.sh
```

## Initialize the dev env

```bash
env:reset
```

!!! info
    This command will:
    
    - create a Python virtual environment using `venv` in a `.env/purplship-server` directory at the root of the project
    - activate the python virtual env
    - install the dev dependencies using `pip install -r requirements.dev.txt`

## Setup the database

```bash
run:db
```

!!! info
    This command starts a Postgresql database using docker-compose

## Run the tests

```bash
test
```

!!! info
    This command run the tests using Python built-in `unittest`

## Working on the webapp

```bash
dev:webapp
```

!!! info
    This command makes a fresh installation of node_modules under `purplship-server/webapp` using yarn,
    then starts the webpack build with watch to automatically rebuild when the webapp is modified and collect
    the build files as django static files.

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

The documentation uses [MkDocs](https://www.mkdocs.org/)

You can start a local doc server using 

```bash
docs
```

!!! info
    This command will run `mkdocs serve`
