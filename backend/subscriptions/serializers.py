from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.serializers import RecipeBriefSerializer
from .models import Follow

User = get_user_model()


class FollowingSerializer(serializers.ModelSerializer):

    is_subscribed = serializers.BooleanField(read_only=True,
                                             default=True)
    recipes_count = serializers.IntegerField(read_only=True)
    recipes = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'is_subscribed',
                  'recipes_count',
                  'recipes')

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        if 'recipes_limit' in request.query_params:
            limit = int(request.query_params['recipes_limit'])
            return RecipeBriefSerializer(recipes[:limit], many=True).data
        return RecipeBriefSerializer(recipes, many=True).data

class FollowCreatedSerializer(FollowingSerializer):

    recipes_count = serializers.SerializerMethodField()
    recipes = RecipeBriefSerializer(many=True)

    def get_recipes_count(self, obj):
        return obj.recipes.all().count()


class FollowWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message=('Нельзя подписаться дважды '
                         'на одного пользователя')
            )
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError('Нельзя подписаться на себя же')
        return data
