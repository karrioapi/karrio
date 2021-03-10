import time
import threading
import schedule

from django.conf import settings

DEFAULT_SCHEDULER_RUN_INTERVAL = getattr(settings, 'DEFAULT_SCHEDULER_RUN_INTERVAL', 3000)


def run_continuously(interval: int = DEFAULT_SCHEDULER_RUN_INTERVAL):
    """Continuously run, while executing pending jobs at each
    elapsed time interval.
    @return cease_continuous_run: threading. Event which can
    be set to cease continuous run. Please note that it is
    *intended behavior that run_continuously() does not run
    missed jobs*. For example, if you've registered a job that
    should run every minute and you set a continuous run
    interval of one hour then your job won't be run 60 times
    at each interval but only once.
    """
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.daemon = True
    continuous_thread.start()
    return cease_continuous_run
