from rest_framework import routers

from .views import RecipeViewSet, IngredientsViewSet, TagViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('recipes',
                RecipeViewSet,
                basename='recipes')
router.register('ingredients',
                IngredientsViewSet,
                basename='ingredients')
router.register('tags',
                TagViewSet,
                basename='tags')

urlpatterns = []
urlpatterns.extend(router.urls)
