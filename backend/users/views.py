from django.contrib.auth import get_user_model
from django.db.models import BooleanField, Case, Value, When
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.pagination import LimitPagination
from subscriptions.models import Follow
from subscriptions.serializers import FollowWriteSerializer, FollowCreatedSerializer


User = get_user_model()


class CustomUserViewSet(UserViewSet):

    FOLLOW_ERROR_MESSAGE = ('Подписки пользователя {user} '
                            'на авторая {author} не существует!')
    pagination_class = LimitPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_queryset(self):
        current_user = self.request.user
        if not current_user.is_authenticated:
            return User.objects.annotate(is_subscribed=Value(False)).all()
        return User.objects.annotate(
            is_subscribed=Case(When(following__user=current_user, then=True),
                               default=False,
                               output_field=BooleanField())).all()

    @action(detail=True,
            url_path='subscribe',
            methods=['POST', 'DELETE'],
            permission_classes=(IsAuthenticated, ))
    def subscribe(self, request, id):
        current_user = self.request.user
        author = get_object_or_404(User, pk=self.kwargs['id'])
        if self.request.method == 'POST':
            data = {'user': current_user.id,
                    'author': author.id}
            serializer = FollowWriteSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serialized_response = FollowCreatedSerializer(current_user)
            return Response(serialized_response.data,
                            status=status.HTTP_201_CREATED)
        instance = Follow.objects.filter(author=author,
                                         user=current_user).get()
        if not instance:
            message = self.FOLLOW_ERROR_MESSAGE.format(author=author,
                                                       user=current_user)
            return Response({'error': message},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
