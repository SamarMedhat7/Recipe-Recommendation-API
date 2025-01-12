from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, Ingredient
from .serializers import RecipeSerializer
from rapidfuzz import fuzz, process
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated

     

class RecipeRecommendationView(APIView):
    def post(self, request):
        input_ingredients = request.data.get('ingredients', [])
        if not input_ingredients:
            return Response({"error": "Please provide ingredients."}, status=400)

        recipes = Recipe.objects.prefetch_related('ingredients')
        suggestions = []

        for recipe in recipes:
            recipe_ingredients = list(recipe.ingredients.values_list('name', flat=True))
            match_score = fuzz.partial_ratio(
                ' '.join(input_ingredients),
                ' '.join(recipe_ingredients)
            )
            if match_score > 70:  # Threshold for recommendation
                suggestions.append({
                    "recipe": recipe.title,
                    "match_score": match_score
                })

        return Response(suggestions)
    


# --- User Management Views ---
class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email)
        token = Token.objects.create(user=user)
        return Response({"message": "User registered successfully.", "token": token.key})
    
class LoginUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})

        return Response({"error": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)   


class UserSavedRecipesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        recipes = request.user.recipes_saved.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)

    def post(self, request):
        recipe_id = request.data.get('recipe_id')
        recipe = Recipe.objects.filter(id=recipe_id).first()

        if not recipe:
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        request.user.recipes_saved.add(recipe)
        return Response({"message": "Recipe saved successfully."})
    





# --- Recipe Management Views ---
class RecipeListView(generics.ListCreateAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer    


class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

class SearchRecipeView(APIView):
    def get(self, request):
        query = request.query_params.get('q', '')
        recipes = Recipe.objects.filter(title__icontains=query)
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)    
    
class FilterRecipesByIngredientsView(APIView):
    def get(self, request):
        ingredients = request.query_params.get('ingredients', '').split(',')
        recipes = Recipe.objects.filter(ingredients__name__in=ingredients).distinct()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)    