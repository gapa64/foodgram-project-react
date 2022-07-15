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

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ('id',
                  'first_name',
                  'last_name',
                  'username',
                  'email',
                  'password')

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SetPassSerializer(serializers.ModelSerializer):

    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
