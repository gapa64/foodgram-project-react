from django.db.models import Count
from django.contrib.auth import get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, viewsets
from rest_framework.permissions import IsAuthenticated

from api.pagination import LimitPagination
from .serializers import FollowingSerializer


User = get_user_model()


class FollowViewSet(mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowingSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = LimitPagination
    ordering = ('following__first_name',)
    filter_backends = (DjangoFilterBackend,
                       filters.OrderingFilter)

    def get_queryset(self):
        current_user = self.request.user
        return User.objects.filter(following__user=current_user).annotate(
            recipes_count=Count('recipes')).all()
