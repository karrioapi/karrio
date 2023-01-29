# -*- encoding: utf-8 -*-
import decouple

KARRIO_HOST = decouple.config("KARRIO_HTTP_HOST", default="0.0.0.0")
KARRIO_PORT = decouple.config("KARRIO_HTTP_PORT", default=5002)

bind = f"{KARRIO_HOST}:{KARRIO_PORT}"
accesslog = "-"
loglevel = "debug"
capture_output = True
enable_stdio_inheritance = True
workers = decouple.config("KARRIO_WORKERS", default=2, cast=int)
