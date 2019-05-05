from django.utils import timezone
from django_cron import CronJobBase, Schedule
from news.service.feed_services import all_feeds_link
from news.service.profile_services import all_profile
from news.utility.populate_utilities import update_feed
from news.utility.recommend_utilities import recommend_based_content


class update_rss(CronJobBase):
    RUN_EVERY_MINS = 15
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


class calculate_keywords(CronJobBase):
    RUN_EVERY_MINS = 30
    RETRY_AFTER_FAILURE_MINS = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS,
                        retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
    code = 'cron.calculate_keywords'

    @staticmethod
    def do():
        print("INI CRON2 - Calculando keywords por cada usuario ({})".format(timezone.now()))

        print('\tBasado en contenido')
        for profile in all_profile():
            print('\t\tINI {}'.format(profile))

            try:
                recommend_based_content(profile)
            except Exception as excep:
                print("Error de cron: {}".format(excep))

        print("FIN CRON2 - Calculando keywords por cada usuario ({})".format(timezone.now()))