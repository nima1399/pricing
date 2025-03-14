from rest_framework import serializers

from crawler.models import User, ValuableObject


class UserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(write_only=True)
    subscribed_valuables = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "email", "subscribed_valuables")
        read_only_fields = ("id",)


class ValuableObjectSerializer(serializers.ModelSerializer):
    title = serializers.CharField(write_only=True)

    class Meta:
        model = ValuableObject
        fields = ("id", "title")
        read_only_fields = ("id",)
