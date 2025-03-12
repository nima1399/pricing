from rest_framework import status
from rest_framework.response import Response


class CeleryService:
    @classmethod
    def run_celery(cls):
        from crawler.management.commands.run_crawler import Command

        if Command.has_run:
            return Response(
                {"status": "Celery is already running!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        else:
            Command().handle()
            return Response({"status": "success"}, status=status.HTTP_200_OK)
