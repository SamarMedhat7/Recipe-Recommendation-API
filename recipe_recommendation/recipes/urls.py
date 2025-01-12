from django.urls import path
from .views import RecipeListView, RecipeRecommendationView ,RegisterUserView, LoginUserView,UserSavedRecipesView,RecipeDetailView,SearchRecipeView,FilterRecipesByIngredientsView,IngredientListView

urlpatterns = [
    path('recommend/', RecipeRecommendationView.as_view(), name='recipe-recommend'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/saved-recipes/', UserSavedRecipesView.as_view(), name='user-saved-recipes'),

    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes/<int:pk>/', RecipeDetailView.as_view(), name='recipe-detail'),
    path('recipes/search/', SearchRecipeView.as_view(), name='recipe-search'),
    path('recipes/filter/', FilterRecipesByIngredientsView.as_view(), name='filter-recipes-by-ingredients'),

    path('ingredients/', IngredientListView.as_view(), name='ingredient-list'),



]