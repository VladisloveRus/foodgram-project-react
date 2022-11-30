from django.contrib import admin
from django.urls import path, include
from recipes import views
from rest_framework.routers import SimpleRouter
recipes_router = SimpleRouter() 
recipes_router.register('tags', views.TagViewSet)
recipes_router.register('recipes', views.RecipeViewSet)


urlpatterns = [
    path('recipes/download_shopping_cart/', views.DownloadShoppingCartView.as_view()),
    path('', include(recipes_router.urls)),
]
