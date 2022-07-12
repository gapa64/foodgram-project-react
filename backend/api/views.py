from django.db.models import Case, Sum, When
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response

from .filters import RecipeFilterSet, NameFilter
from recipes.models import (Recipe, Ingredient, IngredientRecipe,
                            Favorite, Cart, Tag)
from .permissions import AuthorOrReadOnly, StafforReadOnly
from .pagination import LimitPagination
from .serializers import (RecipeReadSerializer, RecipeWriteSerializer,
                          RecipeBriefSerializer, IngredientSerializer,
                          FavoriteSerializer, CartSerializer,
                          TagSerializer)


class TagViewset(viewsets.ModelViewSet):

    queryset = Tag.objects.all()
    permission_classes = (StafforReadOnly,)
    serializer_class = TagSerializer


class IngredientsViewSet(viewsets.ModelViewSet):

    queryset = Ingredient.objects.all()
    permission_classes = (StafforReadOnly,)
    serializer_class = IngredientSerializer
    filter_backends = (NameFilter,)


class RecipeViewSet(viewsets.ModelViewSet):
    FAVORITE_ERROR_MESSAGE = ('Рецепт {recipe} не добавлен в '
                              'избранное пользователя {user}')
    CART_ERROR_MESSAGE = ('Рецепт {recipe} не добавлен в '
                          'корзину пользователя {user}')
    REPORT_CONFIG = {
        'file_name': 'shopping_cart.pdf',
        'title': 'Список Покупок',
        'font_path': 'fonts/FreeSans.ttf',
        'font_name': 'FreeSans',
        'font_size': 12,
        'title_font_size': 25,
        'start_x': 50,
        'start_y': 800,
        'title_x': 200,
        'pagesize': A4
    }
    REPORT_TEMPLATE = '{position}. {ingredient} - {amount}, {unit}'
    DISPOSITION_TEMPLATE = 'attachment; filename="{file_name}"'
    permission_classes = (AuthorOrReadOnly, )
    pagination_class = LimitPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilterSet
    ordering = ('pub_date', )

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
        return self.add_remove_action(
            target_model=Favorite,
            serializer_class=FavoriteSerializer,
            error_message=self.FAVORITE_ERROR_MESSAGE
        )

    @action(detail=True,
            url_path='shopping_cart',
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated, ))
    def shooping_cart(self, request, pk):
        return self.add_remove_action(
            target_model=Cart,
            serializer_class=CartSerializer,
            error_message=self.CART_ERROR_MESSAGE
        )

    @action(detail=False,
            url_path='download_shopping_cart',
            permission_classes=(IsAuthenticated, ))
    def download_shopping_cart(self, request):
        cart = IngredientRecipe.objects.filter(
            recipe__buyers__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(total=Sum('amount')).all()
        return self.render_purchase_list(cart)

    def render_purchase_list(self, purchase_list):
        file_name = self.REPORT_CONFIG['file_name']
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = self.DISPOSITION_TEMPLATE.format(
            file_name=file_name
        )
        canvas = Canvas(response, pagesize=self.REPORT_CONFIG['pagesize'])
        pdfmetrics.registerFont(TTFont(self.REPORT_CONFIG['font_name'],
                                       self.REPORT_CONFIG['font_path']))
        canvas.setFont(self.REPORT_CONFIG['font_name'],
                       self.REPORT_CONFIG['title_font_size'])
        canvas.setTitle(self.REPORT_CONFIG['title'])
        canvas.drawString(x=self.REPORT_CONFIG['title_x'],
                          y=self.REPORT_CONFIG['start_y'],
                          text=self.REPORT_CONFIG['title'])
        position = 1
        x = self.REPORT_CONFIG['start_x']
        y = self.REPORT_CONFIG['start_y'] - 40
        canvas.setFont(self.REPORT_CONFIG['font_name'],
                       self.REPORT_CONFIG['font_size'])
        for purchase in purchase_list:
            if y <= 100:
                y = self.REPORT_CONFIG['start_y']
                canvas.showPage()
            rendered_row = self.REPORT_TEMPLATE.format(
                position=str(position),
                ingredient=purchase['ingredient__name'],
                amount=purchase['total'],
                unit=purchase['ingredient__measurement_unit'])
            canvas.drawString(x, y, rendered_row)
            y -= 20
            position += 1
        canvas.showPage()
        canvas.save()
        return response
