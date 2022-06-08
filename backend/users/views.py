from django.contrib.auth import get_user_model
from django.db.models import Case, When, BooleanField, Value
from djoser.views import UserViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS

from .serializers import CustomUserCreateSerializer, CustomUserReadSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    pagination_class = PageNumberPagination

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_authenticated:
            return User.objects.annotate(is_subscribed=Value(False)).all()
        return User.objects.annotate(
            is_subscribed=Case(When(following__user=current_user, then=True),
                               default=False,
                               output_field=BooleanField())).all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return CustomUserReadSerializer
        return CustomUserCreateSerializer


