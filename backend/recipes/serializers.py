from random import choices
from secrets import choice
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Tag, Recipe, Ingredient, Favorite
from users.serializers import CustomUserSerializer

User = get_user_model()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('pk', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all())
    class Meta:
        model = Ingredient
        fields = ('id', 'amount')


class IngredientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('pk', 'name', 'amount', 'measurement_unit')
        read_only_fields = ('pk', 'name', 'amount', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )
    ingredients = IngredientSerializer(many = True)
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True)
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time')


class RecipeListSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        read_only=True,
    )
    ingredients = IngredientListSerializer(many = True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = Recipe
        fields = ('id', 'author', 'name', 'image', 'text', 'ingredients', 'tags', 'cooking_time')


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