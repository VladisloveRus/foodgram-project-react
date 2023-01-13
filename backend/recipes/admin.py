from django.contrib import admin


from .models import Tag, Ingredient, Recipe, Favorite, ShoppingCart, IngredientAmount


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'color', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):

    list_display = ('pk', 'name', 'measurement_unit')
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):

    list_display = ('pk', 'author', 'name', 'image', 'text', 'cooking_time')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):

    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):

    list_display = ('pk', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):

    list_display = ('pk', 'ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'

