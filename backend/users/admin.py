from django.contrib import admin

from backend.settings import EMPTY_VALUE_DISPLAY as EVD

from .models import CustomUser, Follow

admin.site.register(CustomUser)


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('pk', 'following', 'user')
    empty_value_display = EVD
