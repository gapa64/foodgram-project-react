from django.db.models import Case, When
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe, Ingredient, Favorite, Cart
from .serializers import (RecipeReadSerializer, RecipeWriteSerializer, RecipeBriefSerializer,
                          IngredientSerializer, FavoriteSerializer, CartSerializer)


class IngredientsViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    FAVORITE_ERROR_MESSAGE = ('Рецепт {recipe} не добавлен в '
                              'избранное пользователя {user}')
    CART_ERROR_MESSAGE = ('Рецепт {recipe} не добавлен в '
                          'корзину пользователя {user}')

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_authenticated:
            return Recipe.objects.all()
        recipe_queryset = Recipe.objects.annotate(
            is_favorited=(Case(When(favorited_users__user=current_user,
                                    then=True), default=False))
        ).annotate(
            is_in_shopping_cart=(Case(When(buyers__user=current_user,
                                           then=True), default=False))
        ).all()
        return recipe_queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


    def add_remove_action(self, target_model, serializer_class, error_message):
        current_user = self.request.user
        recipe = get_object_or_404(Recipe, pk=self.kwargs['pk'])
        if self.request.method == 'POST':
            data = {'user': current_user.id,
                    'recipe': recipe.id}
            serializer = serializer_class(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                serialized_response = RecipeBriefSerializer(recipe)
                return Response(serialized_response.data,
                                status=status.HTTP_201_CREATED)
        instance = target_model.objects.filter(recipe=recipe,
                                               user=current_user).get()
        if not instance:
            message = error_message.format(recipe=recipe,
                                           user=current_user)
            return Response({'error': message},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True,
            url_path='favorite',
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated, ))
    def favorite(self, request, pk):
        return self.add_remove_action(target_model=Favorite,
                               serializer_class=FavoriteSerializer,
                               error_message=self.FAVORITE_ERROR_MESSAGE)

    @action(detail=True,
            url_path='shopping_cart',
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated, ))
    def shooping_cart(self, request, pk):
        return self.add_remove_action(target_model=Cart,
                               serializer_class=CartSerializer,
                               error_message=self.CART_ERROR_MESSAGE)
