from rest_framework import generics
from rest_framework.permissions import AllowAny

from crawler.serializers import UserSerializer, ValuableObjectSerializer
from crawler.services.celery_service import CeleryService
from crawler.services.db_service import DatabaseService


class StartCeleryView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        CeleryService.run_celery()


class GetValuableObjectView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        return DatabaseService.get_valuable_objects()


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


class GetEmailsForSubscriptionView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = ValuableObjectSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return DatabaseService.get_emails_for_subscription(serializer.validated_data)
