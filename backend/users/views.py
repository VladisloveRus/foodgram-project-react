from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CustomUserSerializer, FollowSerializer
from .models import Follow
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

User = get_user_model()

#class UsersList(generics.ListCreateAPIView):
#    queryset = User.objects.all()
#    serializer_class = CustomUserSerializer
#
#class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
#    queryset = User.objects.all()
#    serializer_class = CustomUserSerializer
#
##    def subscribe(self, request, pk):
##        user = request.user
##        if request.method == 'POST':
##            data = {'following': pk, 'user': user.id}
##            serializer = FollowSerializer(
##                data=data, context={'request': request}
##            )
##            if not serializer.is_valid():
##                return Response(
##                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
##                )
##            serializer.save()
##            return Response(serializer.data, status=status.HTTP_201_CREATED)
##        following = get_object_or_404(Follow, id=pk)
##        Follow.objects.filter(user=user, following=following).delete()
##        return Response(status=status.HTTP_204_NO_CONTENT)
#
#
#@api_view(['GET'])
#def current_user_view(request):
#    user = get_object_or_404(User, pk=request.user.pk)
#    serializer = CustomUserSerializer(user)
#    return Response(serializer.data)
#

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    # permissions!!!
    
    @action(methods=['get',], detail=False, url_path='me',)
    def me(self, request):
        user = get_object_or_404(User, pk=request.user.pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)

    @action(methods=['get',], detail=False, url_path='subscriptions',)
    def subscriptions(self, request):
        follow = get_object_or_404(Follow, user=request.user.pk)
        serializer = FollowSerializer(follow)
        return Response(serializer.data)

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

