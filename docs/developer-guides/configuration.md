# Configuration

The purplship server instance is configurable using the environment variables. 
purplship server is build with [Django](https://www.djangoproject.com/) 
and most of [deployment settings](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/) 
are relevant to configure this project to few contextual naming differences.

## DEPLOYMENT MODE

- `PURPLSHIP_HOST` | **default:** `0.0.0.0`

The purplship server hostname

- `PURPLSHIP_PORT` | **default:** `5002`

The purplship server port

- `PURPLSHIP_WORKERS` | **default:** `2`

The number of parallel subprocesses for the purplship server

- `DETACHED_WORKER` | [`True`, `False`] | **default:** `False`

Indicate whether the purplship server process should be detached from the background worker process.

!!! warning
    Setting this option to `True` means that you intend to run the background worker process in another container
    or another runtime resource.

- `BACKGROUND_WORKERS` | **default:** `2`

The number of parallel subprocesses for the purplship server background worker

- `DEBUG_MODE`

**values:** | [`True`, `False`] | **default:** `False`

It is important to set `DEBUG_MODE` to `False` in production for security and performance.

!!! abstract ""
    **Is the equivalent of django's `DEBUG` flag**.

- `ALLOWED_HOSTS`

Set a list of authorized host in text separated by commas.

!!! quote ""
    **e.g: "test.com,example.com"**

- `SECRET_KEY`

The secret key must be a unique large value for security reason.

!!! abstract ""
    **Is the equivalent of django's `SECRET_KEY` flag**.

- `USE_HTTPS` | [`True`, `False`] | **default:** `False`

You should set `USE_HTTPS` to `True` when you configure your system in production with SSL.

---

## PROVISIONING

- `ADMIN_EMAIL` | **default:** `admin@example.com`

The default super user admin account email to add when the system start for the first time

- `ADMIN_PASSWORD` | **default:** `demo`

The default super user password

!!! warning
    Make sure to change the password later

---

## LOGGING

[`Learn more`](https://docs.djangoproject.com/en/3.1/topics/logging/)

- `LOG_LEVEL` | [`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`]

The default value is **DEBUG** when **DEBUG_MODE** is **True** else **INFO**

- `LOG_DIR`

Is the log file location.

- `WORKER_DB_DIR`

---

## DATABASE

[`Learn more`](https://docs.djangoproject.com/en/3.1/ref/settings/#databases)

- `DATABASE_HOST`

- `DATABASE_PORT`

- `DATABASE_NAME`

- `DATABASE_ENGINE`

- `DATABASE_USERNAME`

- `DATABASE_PASSWORD`


