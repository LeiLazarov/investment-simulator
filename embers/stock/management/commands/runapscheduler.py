import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from stock import models
import time
import json
import requests
from datetime import datetime
from django.utils.timezone import utc

logger = logging.getLogger(__name__)


def update_quote():
    token = 'buch32v48v6t51vholng'
    stock_list = models.Stock.objects.all()
    for stockItem in stock_list:
        # get data
        quote = requests.get('https://finnhub.io/api/v1/quote?symbol=' + stockItem.symbol + '&token=' + token)

        if quote.status_code == 200:  # fail to get data
            quote = json.loads(quote.text)  # convert data from json to dict
            if quote['t'] != 0:  # the api not return a null dict
                # store it to the local
                stockItem.price = quote['c']
                stockItem.open = quote['o']
                stockItem.close = quote['pc']
                stockItem.high = quote['h']
                stockItem.low = quote['l']
                stockItem.updateAt = datetime.fromtimestamp(int(quote['t'])).astimezone(utc)
                stockItem.save()

        time.sleep(1)


def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            update_quote,
            trigger=CronTrigger(minute="*/10",day_of_week="0-4",hour="14-21"),  # Every 10 minutes
            id="update_quote",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")