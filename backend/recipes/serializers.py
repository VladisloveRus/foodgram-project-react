from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import F
from .models import (
    Tag,
    Recipe,
    Ingredient,
    Favorite,
    ShoppingCart,
    IngredientAmount,
)
import base64
from django.core.files.base import ContentFile
from users.serializers import CustomUserSerializer

# from drf_extra_fields.fields import Base64ImageField

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = ('id', 'name', 'color', 'slug')


class IngredientForViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()
    measurement_unit = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)

    def get_measurement_unit(self, obj):
        return Ingredient.objects.get(id=obj.id).measurement_unit

    def get_name(self, obj):
        return Ingredient.objects.get(id=obj.id).name

    def to_representation(self, value):
        representation = super().to_representation(value)
        ingredient_amount = IngredientAmount.objects.filter(
            recipe=value.recipe.id
        )
        ingredients = []
        for ingredient in ingredient_amount:
            id = ingredient.ingredient.id
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            ingredients.append(
                {
                    'id': id,
                    'name': name,
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            )
        representation[ingredients] = ingredients
        return representation

    class Meta:
        model = IngredientAmount
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit',
        )
        read_only_fields = ('name', 'measurement_unit')


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    author = CustomUserSerializer(
        read_only=True,
    )
    ingredients = IngredientListSerializer(
        many=True,
    )
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    @staticmethod
    def create_ingredients(ingredients, recipe):
        for ingredient in ingredients:
            IngredientAmount.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount'],
            )

    @staticmethod
    def create_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.create_ingredients(ingredients, recipe)
        return recipe

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )
        read_only_fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeListSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)
    author = CustomUserSerializer(
        read_only=True,
    )

    ingredients = serializers.SerializerMethodField(read_only=True)

    def get_ingredients(self, obj):
        ingredient_amount = IngredientAmount.objects.filter(recipe=obj)
        data = []
        for ingredient in ingredient_amount:
            id = ingredient.ingredient.id
            amount = ingredient.amount
            name = ingredient.ingredient.name
            measurement_unit = ingredient.ingredient.measurement_unit
            data.append(
                {
                    'id': id,
                    'name': name,
                    'measurement_unit': measurement_unit,
                    'amount': amount,
                }
            )
        return data

    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Favorite.objects.filter(user=user, recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return ShoppingCart.objects.filter(user=user, recipe=obj).exists()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField(read_only=True, required=False)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True
    )
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    cooking_time = serializers.SerializerMethodField(read_only=True)

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    #    image = serializers.SerializerMethodField()

    #    def get_image(self, obj):
    #        return (
    #            obj.recipe.image.url
    #        )  # Возможно не так должно быть, но пока пусть будет урл

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time

    class Meta:
        model = Favorite
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')


class ShoppingCartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(), write_only=True
    )
    id = serializers.SerializerMethodField(read_only=True)
    name = serializers.SerializerMethodField(read_only=True)
    cooking_time = serializers.SerializerMethodField(read_only=True)
    image = Base64ImageField(read_only=True, required=False)
    #    image = serializers.SerializerMethodField()

    #    def get_image(self, obj):
    #        return (
    #            obj.recipe.image.url
    #        )  # Возможно не так должно быть, но пока пусть будет урл

    def get_id(self, obj):
        return obj.recipe.id

    def get_name(self, obj):
        return obj.recipe.name

    def get_cooking_time(self, obj):
        return obj.recipe.cooking_time

    class Meta:
        model = ShoppingCart
        fields = ('user', 'recipe', 'id', 'name', 'image', 'cooking_time')
