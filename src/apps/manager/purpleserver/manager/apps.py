from django.apps import AppConfig


class ManagerConfig(AppConfig):
    name = 'purpleserver.manager'

    def ready(self):
        from purpleserver.manager import jobs
        jobs.start_schedulers()
