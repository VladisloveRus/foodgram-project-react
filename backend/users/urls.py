from django.contrib import admin
from django.urls import include, path
from djoser.views import TokenCreateView, TokenDestroyView, UserViewSet
from rest_framework.routers import SimpleRouter

from users import views

users_router = SimpleRouter()

users_router.register('users', views.CustomUserViewSet)

urlpatterns = [
    path('auth/token/login/', TokenCreateView.as_view(), name='login'),
    path('auth/token/logout/', TokenDestroyView.as_view(), name='logout'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path(
        'users/set_password/',
        UserViewSet.as_view({'post': 'set_password'}),
        name='set-password',
    ),
    path('', include(users_router.urls)),
]
