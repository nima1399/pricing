from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from crawler.models import ValuableObject, User
from crawler.serializers import UserSerializer


class DatabaseService:
    @classmethod
    def get_valuable_object_titles(cls):
        active_objects = ValuableObject.active_objects.all()
        titles = [obj.title for obj in active_objects]
        serialized_data = serialize('json', titles)
        return Response(serialized_data, status=status.HTTP_200_OK)

    @classmethod
    def register_user(cls, user_data):
        if User.active_objects.filter(email=user_data['email']).exists():
            return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)
        user = User.active_objects.create_user(email=user_data['email'], subscribed_valuables=user_data['subscribed_valuables'])
        user.save()
        return Response({"id": user.id}, status=status.HTTP_201_CREATED)

    @classmethod
    def add_subscription(cls, user_data):
        user = get_object_or_404(User, email=user_data['email'])
        for subscribe_id in user_data['subscribed_valuables']:
            if not ValuableObject.active_objects.filter(id=subscribe_id).exists():
                return Response({"error": f"Valuable object with id {subscribe_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            valuable = ValuableObject.active_objects.get(id=subscribe_id)
            if not user.subscribed_valuables.filter(ValuableObject.id == subscribe_id).exists():
                user.subscribed_valuables.add(valuable)
        user.save()
        return Response({"id": user.id}, status=status.HTTP_200_OK)

    @classmethod
    def remove_subscription(cls, user_data):
        user = get_object_or_404(User, email=user_data['email'])
        for subscribe_id in user_data['subscribed_valuables']:
            if not ValuableObject.active_objects.filter(id=subscribe_id).exists():
                return Response({"error": f"Valuable object with id {subscribe_id} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
            valuable = ValuableObject.active_objects.get(id=subscribe_id)
            if user.subscribed_valuables.filter(ValuableObject.id == subscribe_id).exists():
                user.subscribed_valuables.remove(valuable)
        user.save()
        return Response({"id": user.id}, status=status.HTTP_200_OK)