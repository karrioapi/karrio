# -*- encoding: utf-8 -*-
import decouple

PURPLSHIP_HOST = decouple.config("PURPLSHIP_HOST", default="0.0.0.0")
PURPLSHIP_PORT = decouple.config("PURPLSHIP_PORT", default=5002)

bind = f'{PURPLSHIP_HOST}:{PURPLSHIP_PORT}'
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
workers = decouple.config("PURPLSHIP_WORKERS", default=2, cast=int)
