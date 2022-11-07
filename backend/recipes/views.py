from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Tag, Recipe, Favorite
from .serializers import (
    TagSerializer,
    RecipeSerializer,
    RecipeListSerializer,
    FavoriteSerializer,
)
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # permissions!!!

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @action(
        methods=[
            'post',
            'delete',
        ],
        detail=True,
        url_path='favorite',
    )
    def favorite(self, request, pk):
        user = request.user
        if request.method == 'POST':
            data = {'recipe': pk, 'user': user.id}
            serializer = FavoriteSerializer(
                data=data, context={'request': request}
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, id=pk)
        Favorite.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#class FavoriteApiView(APIView):
#    def post(self, request, recipe_id):
#        data = {'recipe': recipe_id, 'user': request.user.id}
#        serializer = FavoriteSerializer(
#            data=data, context={'request': request}
#        )
#        if not serializer.is_valid():
#            return Response(
#                serializer.errors, status=status.HTTP_400_BAD_REQUEST
#            )
#        serializer.save()
#        return Response(serializer.data, status=status.HTTP_201_CREATED)
#
#    def delete(self, request, recipe_id):
#        user = request.user
#        recipe = get_object_or_404(Recipe, id=recipe_id)
#        Favorite.objects.filter(user=user, recipe=recipe).delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)
