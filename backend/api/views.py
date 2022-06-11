from django.db.models import Case, When, BooleanField, Value
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Recipe, Ingredient, Favorite
from .serializers import RecipeReadSerializer, RecipeWriteSerializer, IngredientSerializer, FavoriteSerializer



class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    pass

class IngredientsViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    FAVORITE_ERROR_MESSAGE = ('Рецепт {recipe} не добавлен в '
                              'избранное пользователя {user}')

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_authenticated:
            return Recipe.objects.all()
        recipe_queryset = Recipe.objects.annotate(
            is_favorited=(Case(When(favorited_users__user=current_user,
                                    then=True), default=False))
        ).annotate(
            is_in_shopping_cart=(Case(When(cart__buyer=current_user,
                                           then=True), default=False))
        ).all()
        return recipe_queryset

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True,
            url_path='favorite',
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated, ))
    def favorite(self, request, pk):
        current_user = self.request.user
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        if self.request.method == 'POST':
            serializer = FavoriteSerializer(data=self.request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=current_user,
                                recipe=recipe)
                return Response(serializer.data,
                                status=status.HTTP_201_CREATED)
        favorite = Favorite.objects.filter(recipe=recipe,
                                           user=current_user)
        if not favorite:
            message = self.FAVORITE_ERROR_MESSAGE.format(recipe=recipe,
                                                         user=current_user)
            return Response({'error': message},
                            status=status.HTTP_400_BAD_REQUEST)
        favorite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
