from django.contrib import admin
from django.urls import path, include
from djoser.views import TokenCreateView, UserViewSet, TokenDestroyView
from users import views
from rest_framework.routers import SimpleRouter

users_router = SimpleRouter()

users_router.register('users', views.UserViewSet)

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
