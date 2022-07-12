from django.contrib.auth import get_user_model
from rest_framework import serializers


User = get_user_model()


class CustomUserReadSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'id',
                  'is_subscribed')


class CustomUserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password')


class SetPassSerializer(serializers.ModelSerializer):

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
