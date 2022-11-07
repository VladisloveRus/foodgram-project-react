from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Follow

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    def get_is_subscribed(self, obj):
        if obj.following.exists():
            return True
        return False

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name', 'is_subscribed')


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
    def get_is_subscribed(self, obj):
        return True

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
        )
