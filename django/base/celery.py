"""
This module initializes the Celery app and ensures that the
Django app is always imported when Celery starts.
"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import django

django.setup()

from crawler.tasks import crawl


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")


app = Celery("base")

# Configure Celery using settings from Django settings.py.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


# Configure periodic tasks
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls crawl every 30 seconds
    sender.add_periodic_task(30.0, crawl.s(), name="Crawler")
