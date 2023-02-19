from django.urls import include, path
from rest_framework.routers import SimpleRouter

from recipes import download, views

recipes_router = SimpleRouter()
recipes_router.register('ingredients', views.IngredientViewSet)
recipes_router.register('tags', views.TagViewSet)
recipes_router.register('recipes', views.RecipeViewSet)


urlpatterns = [
    path(
        'recipes/download_shopping_cart/',
        download.DownloadShoppingCartView.as_view(),
    ),
    path('', include(recipes_router.urls)),
]
