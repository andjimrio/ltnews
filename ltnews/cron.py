from django.utils import timezone
from django_cron import CronJobBase, Schedule
from news.service.feed_services import all_feeds_link
from news.utility.populate_utilities import update_feed


class update_rss(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.update_rss'

    @staticmethod
    def do():
        print("INI CRON1 - Actualizando entradas ({})".format(timezone.now()))
        for link in all_feeds_link():
            try:
                update_feed(link, printer=True)
            except Exception as excep:
                print("Error de cron: {}".format(excep))

        print("FIN CRON1 - Actualizando entradas ({})".format(timezone.now()))