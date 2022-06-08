from django.db.models import Case, When, BooleanField, Value
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated

from recipes.models import Recipe, Ingredient
from .serializers import RecipeReadSerializer, RecipeWriteSerializer, IngredientSerializer



class CreateDeleteViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    pass

class IngredientsViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    #queryset = Recipe.objects.all()

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_authenticated:
            return Recipe.objects.all()
        recipe_queryset = Recipe.objects.annotate(
            is_favorited=(Case(When(favorite__user=current_user,
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

    def _get_recipe(self):
        recipe_id = self.kwargs.get('title_id')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        return recipe

    @action(detail=True,
            url_path='favorite',
            methods=['POST'],
            permission_class=IsAuthenticated)
    def favorite(self):
        current_user = self.request.user
        recipe = self._get_recipe()
        if current_user.favorite.recipes.filter(recipe=recipe).exists()
            pass




    '''


class FavoriteViewSet(CreateDeleteViewSet):

    serializer = FavoriteSerializer



    def perform_create(self, serializer):
        recipe = self._get_recipe()
        user = self.request.user
        pass

    def perform_destroy(self, instance):
        recipe = self._get_recipe()
        user = self.request.user


'''