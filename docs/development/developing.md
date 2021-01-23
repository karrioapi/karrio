## Requirements

- A bash compatible shell (OSX, Linux or Windows Linux subsystem)

## Clone the repo

```bash
git clone git@github.com:PurplShip/purplship.git
```

## Source the `bash` script

```bash
cd purplship

source ./script.sh
```

## Initialize the dev env

```bash
env:reset
```

!!! info
    This command will:
    
    - create a Python virtual environment using `venv` in a `.env/purplship` directory at the root of the project
    - activate the python virtual env
    - install the dev dependencies using `pip install -r requirements.dev.txt`

## Run the tests

```bash
test
```

!!! info
    This command run the tests using Python built-in `unittest`

## Run the type checker

```bash
typecheck
```

!!! info
    This command run type checker provided by `mypy`

## Run the type checker

```bash
typecheck
```

!!! info
    This command run type checker provided by `mypy`

## Docs

First, make sure you set up your environment as described above, that will install all the requirements.

The documentation uses [MkDocs](https://www.mkdocs.org/)

You can start a local doc server using 

```bash
docs
```

!!! info
    This command will run `mkdocs serve`
