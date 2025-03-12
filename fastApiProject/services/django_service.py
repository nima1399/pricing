import requests
from decouple import config
from typing_extensions import List


class DjangoService:
    DJANGO_API_URL = config("DJANGO_API_URL")

    @classmethod
    def get_emails(cls, valuable_object: str) -> List:
        url = cls.DJANGO_API_URL + "get-emails-for-subscription/"
        params = {"title": valuable_object}
        response = requests.get(url, params=params)
        return response.json()
