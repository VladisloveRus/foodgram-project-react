from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tag, Recipe, Ingredient, Favorite, ShoppingCart, IngredientAmount
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('pk', 'name', 'color', 'slug')


#class IngredientAmountSerializer(serializers.ModelSerializer):
#    pass

# Кажется, этот кусок больше не нужен
#class IngredientSerializer(serializers.ModelSerializer):
#    id = serializers.PrimaryKeyRelatedField(
#        queryset=Ingredient.objects.all())
#    amount = serializers.IntegerField(min_value=1)
#    class Meta:
#        model = IngredientAmount
#        fields = ('id', 'amount')


class IngredientListSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()
    def get_amount(self, obj):
        return IngredientAmount.objects.get(ingredient=obj.pk).amount
    class Meta:
        model = Ingredient
        fields = ('pk', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('pk', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    ingredients = IngredientListSerializer(many = True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    def get_is_favorited(self, obj):
        if obj.favorite.exists():
            return True
        return False
    def get_is_in_shopping_cart(self, obj):
        if obj.shopping_cart.exists():
            return True
        return False
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time', )


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
    )
    ingredients = IngredientListSerializer(many = True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    def get_is_favorited(self, obj):
        if obj.favorite.exists():
            return True
        return False
    def get_is_in_shopping_cart(self, obj):
        if obj.shopping_cart.exists():
            return True
        return False
    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited', 'is_in_shopping_cart', 'name', 'image', 'text', 'cooking_time', )


class FavoriteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True)
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()
    def get_id(self, obj):
        return obj.recipe.id
    def get_name(self, obj):
        return obj.recipe.name
    def get_image(self, obj):
        return obj.recipe.image.url #Возможно не так должно быть, но пока пусть будет урл
    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
    class Meta:
        model = Favorite
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')

class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True)
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cooking_time = serializers.SerializerMethodField()
    def get_id(self, obj):
        return obj.recipe.id
    def get_name(self, obj):
        return obj.recipe.name
    def get_image(self, obj):
        return obj.recipe.image.url #Возможно не так должно быть, но пока пусть будет урл
    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time
    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')
