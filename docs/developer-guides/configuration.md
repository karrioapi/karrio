# Configuration

The purplship server instance is configurable using the environment variables. 
purplship server is a [Django](https://www.djangoproject.com/) based project 
and most of [deployment settings](https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/) 
are relevant to configure this project with few contextual naming differences.

## DEPLOYMENT

- **`PURPLSHIP_HOST`** | **default:** `0.0.0.0`

The purplship server hostname

- **`PURPLSHIP_PORT`** | **default:** `5002`

The purplship server port

- **`PURPLSHIP_WORKERS`** | **default:** `2`

The number of parallel subprocesses for the purplship server

- **`DETACHED_WORKER`** | [`True`, `False`] | **default:** `False`

Indicate whether the purplship server process should be detached from the background worker process.

!!! warning
    Setting this option to `True` means that you intend to run the background worker process in another container
    or another runtime resource.

- **`BACKGROUND_WORKERS`** | **default:** `2`

The number of parallel subprocesses for the purplship server background worker

- **`DEBUG_MODE`** | [`True`, `False`] | **default:** `False`

It is important to set `DEBUG_MODE` to `False` in production for security and performance.

!!! abstract ""
    **Is the equivalent of django's `DEBUG` flag**.

- **`ALLOWED_HOSTS`**

Set a list of authorized host in text separated by commas.

!!! quote ""
    **e.g: "test.com,example.com"**

- **`SECRET_KEY`**

The secret key must be a unique large value for security reason.

!!! abstract ""
    **Is the equivalent of django's `SECRET_KEY` flag**.

- **`USE_HTTPS`** | [`True`, `False`] | **default:** `False`

You should set `USE_HTTPS` to `True` when you configure your system in production with SSL.

---

## PROVISIONING

- **`ADMIN_EMAIL`** | **default:** `admin@example.com`

The default super user admin account email to add when the system start for the first time

- **`ADMIN_PASSWORD`** | **default:** `demo`

The default super user password

!!! warning
    Make sure to change the password later

---

## LOGGING

- **`LOG_LEVEL`** | [`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`]

The default value is **DEBUG** when **DEBUG_MODE** is **True** else **INFO**

- **`LOG_DIR`**

Is the log file location.

- **`WORKER_DB_DIR`**

The purplship server background worker persists events to process so that
even after a shutdown, they can recover tasks and process them.

!!! hint
    When you are using a container, you might want to mount this folder
    on a volume so that they can be recovered when the container shuts down.

---

## DATABASE

[`Learn more`](https://docs.djangoproject.com/en/3.2/ref/settings/#databases)

- **`DATABASE_HOST`** | **default:** `db`

The database host

!!! hint ""
    the database host can be an IP address or a hostname

- **`DATABASE_PORT`** | **default:** `5432`

The database port

- **`DATABASE_NAME`** | **default:** `db`

The database name

- **`DATABASE_ENGINE`** | [`postgresql_psycopg2`, `postgresql`, `mysql`, `oracle`] | **default:** `postgresql_psycopg2`

The database engine or database type

!!! warning
    Currently, purplship server has been tested with `PostgreSQL`

- **`DATABASE_USERNAME`** | **default:** `postgres`

The database connection' user

- **`DATABASE_PASSWORD`** | **default:** `postgres`

The database connection' password
