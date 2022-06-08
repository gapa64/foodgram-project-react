from django.urls import include, path, re_path
from rest_framework import routers
from .views import RecipeViewSet, IngredientsViewSet, FavoriteVieSet

app_name = 'users'

router = routers.DefaultRouter()
router.register(r'recipes/(?P<recip_id>\d+)/favorite',
                Favorite,
                basename='favorite')
router.register('recipes',
                RecipeViewSet,
                basename='recipes')
router.register('ingredients',
                IngredientsViewSet,
                basename='ingredients')

'''
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'

'''

urlpatterns = router.urls

#urlpatterns = [
#    re_path(r'users/', include('users.urls')),
#]
