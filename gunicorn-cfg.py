# -*- encoding: utf-8 -*-
import decouple

PURPLSHIP_PORT = decouple.config("PURPLSHIP_PORT", default=5002)

bind = f'0.0.0.0:{PURPLSHIP_PORT}'
accesslog = '-'
loglevel = 'debug'
capture_output = True
enable_stdio_inheritance = True
reload = decouple.config("RELOAD", default=False)
workers = decouple.config("PURPLSHIP_WORKERS", default=2)
