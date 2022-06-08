
from django.urls import include, path, re_path
from rest_framework import routers
from .views import CustomUserViewSet

app_name = 'users'

router = routers.DefaultRouter()
router.register('', CustomUserViewSet, basename='users')

urlpatterns = router.urls


'''
from django.urls import include, path
from djoser.views import UserViewSet

from rest_framework_simplejwt import views

#re_path(r"^jwt/create/?", views.TokenObtainPairView.as_view(), name="jwt-create"),
#re_path(r"^jwt/refresh/?", views.TokenRefreshView.as_view(), name="jwt-refresh"),
#re_path(r"^jwt/verify/?", views.TokenVerifyView.as_view(), name="jwt-verify"),

urlpatterns = [
    path('', include('djoser.urls')),
#    path('token/', UserViewSet.as_view({'post': 'create'}), name="register"),
    path('token/login/',
         views.TokenObtainPairView.as_view(),
         name='jwt-create'),
    path('token/logout/',
         views.TokenRefreshView.as_view(),
         name='jwt-create')
]
'''