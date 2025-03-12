import subprocess

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run Celery worker and Celery beat in separate terminal windows"
    has_run = False

    def handle(self, *args, **kwargs):
        if self.has_run:
            self.stdout.write(self.style.WARNING("Celery is already running!"))
            return
        # Open Celery worker in a new terminal
        self.stdout.write(self.style.SUCCESS("Starting Celery worker..."))
        subprocess.Popen(
            [
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                "celery -A base worker --loglevel=debug; exec bash",
            ]
        )

        # Open Celery beat in a new terminal
        self.stdout.write(self.style.SUCCESS("Starting Celery beat..."))
        subprocess.Popen(
            [
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                "celery -A base beat --loglevel=debug; exec bash",
            ]
        )

        self.stdout.write(self.style.SUCCESS("Celery started in separate terminals!"))
        Command.has_run = True
