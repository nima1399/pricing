import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Run Celery worker and Celery beat in separate terminal windows"

    def handle(self, *args, **kwargs):
        # Open Celery worker in a new terminal
        self.stdout.write(self.style.SUCCESS("Starting Celery worker..."))
        subprocess.Popen(
            [
                "gnome-terminal",
                "--",
                "bash",
                "-c",
                "celery -A base worker --loglevel=info; exec bash",
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
                "celery -A base beat --loglevel=info; exec bash",
            ]
        )

        self.stdout.write(self.style.SUCCESS("Celery started in separate terminals!"))
