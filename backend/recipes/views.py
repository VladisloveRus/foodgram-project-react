from django.shortcuts import render, get_object_or_404, HttpResponse
from rest_framework import permissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from .models import Tag, Recipe, Favorite, ShoppingCart, IngredientAmount
from .permissions import OwnerOrReadOnly, ReadOnly
from .serializers import (
    TagSerializer,
    RecipeSerializer,
    RecipeListSerializer,
    FavoriteSerializer,
    ShoppingCartSerializer,
)
from rest_framework import generics, status, mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from rest_framework.views import APIView


class TagViewSet(ReadOnlyModelViewSet):
    permission_classes = (ReadOnly)
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (OwnerOrReadOnly(),)
        return super().get_permissions() 

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

    @action(
        methods=[
            'post',
            'delete',
        ],
        detail=True,
        url_path='shopping_cart',
    )
    def shopping_cart(self, request, pk):
        user = request.user
        if request.method == 'POST':
            data = {'recipe': pk, 'user': user.id}
            serializer = ShoppingCartSerializer(
                data=data, context={'request': request}
            )
            if not serializer.is_valid():
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        recipe = get_object_or_404(Recipe, id=pk)
        ShoppingCart.objects.filter(user=user, recipe=recipe).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DownloadShoppingCartView(APIView):
    permission_classes = (OwnerOrReadOnly)
    def get(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recipe_list = []
        for cart in shopping_cart:
            recipe = cart.recipe
            recipe_list.append(recipe.pk)

        lines = []
        amount = []
        ingredient_amount_dict = {}
        count = 0
        for recipe_pk in recipe_list:
            ingredient_amount_list = IngredientAmount.objects.filter(
                recipe=recipe_pk
            )
            for ingredient_amount in ingredient_amount_list:
                if (
                    ingredient_amount.ingredient.name
                    in ingredient_amount_dict.keys()
                ):
                    ingredient_amount_dict[
                        ingredient_amount.ingredient.name
                    ] = (
                        ingredient_amount_dict[
                            ingredient_amount.ingredient.name
                        ]
                        + ingredient_amount.amount
                    )
                else:
                    ingredient_amount_dict[
                        ingredient_amount.ingredient.name
                    ] = ingredient_amount.amount
                    amount.append(
                        ingredient_amount.ingredient.measurement_unit
                    )
        for ingregient in ingredient_amount_dict:
            lines.append(
                ingregient
                + ' - '
                + str(ingredient_amount_dict[ingregient])
                + ' '
                + amount[count]
                + f'\n'
            )
            count += 1
        response = HttpResponse(lines, 'Content-Type: text/plain')
        response['Content-Disposition'] = 'attachment; filename="BuyList.txt"'
        return response
