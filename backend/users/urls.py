from rest_framework import routers
from .views import CustomUserViewSet
from subscriptions.views import FollowViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('subscriptions', FollowViewSet, basename='subscriptions')
router.register('', CustomUserViewSet, basename='users_dj')

urlpatterns = []
urlpatterns.extend(router.urls)
