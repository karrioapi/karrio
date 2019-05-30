import os

app_stage = os.environ.get('APP_STAGE', 'development')
if app_stage == 'production':
    from .production import *
elif app_stage == 'containerized':
    from .containerized import *
else:
    from .development import *

from purplship_config import *
