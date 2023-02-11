from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Recipe
from rest_framework import serializers

from .models import Follow

User = get_user_model()


class FollowRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, following=obj.id).exists()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'password',
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class SetPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    following = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    email = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    first_name = serializers.SerializerMethodField()
    last_name = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=user, following=obj.following
        ).exists()  # было following=obj.id. Если что-то сломалось - вернуть

    def get_email(self, obj):
        return obj.following.email

    def get_id(self, obj):
        return obj.following.id

    def get_username(self, obj):
        return obj.following.username

    def get_first_name(self, obj):
        return obj.following.first_name

    def get_last_name(self, obj):
        return obj.following.last_name

    def get_recipes(self, obj):
        queryset = Recipe.objects.filter(author=obj.following)
        return FollowRecipeSerializer(queryset, many=True).data

    class Meta:
        model = Follow
        fields = (
            'user',
            'following',
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
        )
