from django.urls import path
from .views import RecipeListView, RecipeRecommendationView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recommend/', RecipeRecommendationView.as_view(), name='recipe-recommend'),
]