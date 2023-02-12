from django.contrib import admin

from .models import CustomUser, Follow
from backend.settings import EMPTY_VALUE_DISPLAY as EVD

admin.site.register(CustomUser)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'following', 'user')
    empty_value_display = EVD
