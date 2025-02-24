
from django.core.serializers import serialize
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from crawler.api_services.db_service import DatabaseService
from crawler.models import ValuableObject
from crawler.api_services.celery_service import CeleryService
from crawler.serializers import UserSerializer


class StartCeleryView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        CeleryService.run_celery()

class GetValuableObjectView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        DatabaseService.get_valuable_object_titles()


class RegisterUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DatabaseService.register_user(serializer.validated_data)

class AddSubscriptionView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DatabaseService.add_subscription(serializer.validated_data)

class RemoveSubscriptionView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return DatabaseService.remove_subscription(serializer.validated_data)