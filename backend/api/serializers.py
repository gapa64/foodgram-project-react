from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from recipes.models import Recipe, Ingredient, IngredientRecipe, Tag, Favorite
from users.serializers import CustomUserReadSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientRecipeSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientRecipe
        fields = ('id', 'amount')

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError(
                'Количество ингредиента должно быть больше 0')
        return amount

class IngredientRecipeReadSerializer(serializers.ModelSerializer):

    id = serializers.PrimaryKeyRelatedField(
        source='ingredient', read_only=True
    )
    measurement_unit = serializers.CharField\
        (source='ingredient.measurement_unit'
    )
    name = serializers.CharField(
        source='ingredient.name'
    )

    class Meta:
        model = IngredientRecipe
        fields = ('id',
                  'amount',
                  'measurement_unit',
                  'name')


class RecipeWriteSerializer(serializers.ModelSerializer):

    author = SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )
    ingredients = IngredientRecipeSerializer(
        many=True,
    )
    cooking_time = serializers.IntegerField()

    class Meta:
        fields = '__all__'
        model = Recipe

    def validate_cooking_time(self, cooking_time):
        if cooking_time >= 1:
            return cooking_time
        raise serializers.ValidationError('Время приготовления не может '
                                          'быть меньше 1')

    def validate_ingredients(self, ingredients):
        unique_ingredients = set()
        for ingredient, amount in ingredients:
            if ingredient in unique_ingredients:
                raise serializers.ValidationError('Ингредиент должен '
                                                  'быть уникальным')
            unique_ingredients.add(ingredient)
        return ingredients

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            IngredientRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        super().update(instance, validated_data)
        instance.tags.set(tags)
        ingredients.all().delete()
        self.create_ingredients(ingredients, instance)
        instance.save()
        return instance


class RecipeReadSerializer(serializers.ModelSerializer):
    author = CustomUserReadSerializer()
    ingredients = IngredientRecipeReadSerializer(many=True,
                                                 source='ingredientrecipe_set')
    tags = TagSerializer(many=True)
    is_favorited = serializers.BooleanField(
        default=False,
        read_only=True
    )
    is_in_shopping_cart = serializers.BooleanField(
        default=False,
        read_only=True
    )
    class Meta:
        fields = '__all__'
        model = Recipe

class FavoriteSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True,
                                              required=False)
    recipe = serializers.PrimaryKeyRelatedField(read_only=True,
                                                required=False)

    class Meta:
        fields = ('user', 'recipe')
        model = Favorite

    def create(self, validated_data):
        recipe = validated_data['recipe']
        user = validated_data['user']
        if Favorite.objects.filter(recipe=recipe,
                                   user=user).exists():
            raise serializers.ValidationError('Нельзя добавить рецепт '
                                              'в избранное дважды')
        favorite = Favorite.objects.create(user=user, recipe=recipe)
        return favorite




    '''   
    def validate(self, data):
        print(data)
        recipe = data['recipe']
        user = data['user']
        if Favorite.objects.filter(recipe=recipe,
                                   user=user).exists():
            raise serializers.ValidationError('Нельзя добавить рецепт'
                                              'в избранное дважды')
        return attrs

    def validate(self, attrs):
        recipe = attrs['recipe']
        if attrs.user.favorite.recipes.filter(recipe=recipe).exists():
            raise serializers.ValidationError('Нельзя добавить рецепт'
                                              'в избранное дважды')
    '''