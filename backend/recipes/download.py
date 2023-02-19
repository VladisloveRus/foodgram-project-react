from django.shortcuts import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import IngredientAmount, ShoppingCart
from .permissions import AuthorOrReadOnly


class DownloadShoppingCartView(APIView):
    permission_classes = (AuthorOrReadOnly,)

    def get(self, request):
        shopping_cart = ShoppingCart.objects.filter(user=request.user)
        recipe_list = []
        for cart in shopping_cart:
            recipe = cart.recipe
            recipe_list.append(recipe.pk)
        if recipe_list == []:
            return Response(status=status.HTTP_204_NO_CONTENT)

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
                + '\n'
            )
            count += 1
        return HttpResponse(
            lines,
            headers={
                'Content-Type': 'text/plain',
                'Content-Disposition': 'attachment; filename="BuyList.txt"',
            },
        )
