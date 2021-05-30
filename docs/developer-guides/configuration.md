# Configuration

The Purplship server instance is configurable using the environment variables. 
Purplship server is build with [Django](https://www.djangoproject.com/) 
and most of [deployment settings](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/) 
are relevant to configure this project to few contextual naming differences.

## DEPLOYMENT MODE

- `DEBUG_MODE`

**values:** [`True`, `False`] | **default:** `False`

**Is the equivalent of django's `DEBUG` flag**.

It is important to set `DEBUG_MODE` to `False` in production for security and performance.

- `ALLOWED_HOSTS`

Set a list of authorized host in text separated by commas.

**e.g: "test.com,domain.com"**

- `SECRET_KEY`

**Is the equivalent of django's `SECRET_KEY` flag**.

The secret key must be a unique large value for security reason.

- `USE_HTTPS`

**values:** [`True`, `False`] | **default:** `False`

You should set `USE_HTTPS` to `True` when you configure your system in production with SSL.

---

## LOGGING

[`Learn more`](https://docs.djangoproject.com/en/3.1/topics/logging/)

- `LOG_LEVEL`

**values:** [`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`]

The default value is **DEBUG** when **DEBUG_MODE** is **True** else **INFO**

- `LOG_PATH`

Is the log file location.

---

## DATABASE

[`Learn more`](https://docs.djangoproject.com/en/3.1/ref/settings/#databases)

- `DATABASE_HOST`

- `DATABASE_PORT`

- `DATABASE_NAME`

- `DATABASE_ENGINE`

- `DATABASE_USERNAME`

- `DATABASE_PASSWORD`


