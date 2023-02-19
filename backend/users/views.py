from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.permissions import ReadOnly
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Follow
from .serializers import CustomUserSerializer, FollowSerializer

User = get_user_model()


class CustomUserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    @action(
        methods=[
            'get',
        ],
        detail=False,
        url_path='me',
    )
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = CustomUserSerializer(user, context={'request': request})
        return Response(serializer.data)

    @action(
        methods=[
            'get',
        ],
        detail=False,
        url_path='subscriptions',
    )
    def subscriptions(self, request):
        queryset = Follow.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(
        methods=[
            'post',
            'delete',
        ],
        detail=True,
        url_path='subscribe',
    )
    def subscribe(self, request, pk):
        user = request.user
        if request.method == 'POST':
            data = {'following': pk, 'user': user.id}
            serializer = FollowSerializer(
                data=data, context={'request': request}
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        following = get_object_or_404(User, id=pk)
        Follow.objects.filter(user=user, following=following).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
