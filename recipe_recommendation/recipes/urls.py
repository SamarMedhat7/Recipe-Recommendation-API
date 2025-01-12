from django.urls import path
from .views import RecipeListView, RecipeRecommendationView ,RegisterUserView, LoginUserView,UserSavedRecipesView

urlpatterns = [
    path('recipes/', RecipeListView.as_view(), name='recipe-list'),
    path('recommend/', RecipeRecommendationView.as_view(), name='recipe-recommend'),

    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('user/saved-recipes/', UserSavedRecipesView.as_view(), name='user-saved-recipes'),


]