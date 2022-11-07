from django.contrib import admin
from django.urls import path, include
from djoser.views import TokenCreateView, UserViewSet, TokenDestroyView
from rest_framework.routers import SimpleRouter
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/', include('users.urls')),
    path('api/', include('recipes.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
