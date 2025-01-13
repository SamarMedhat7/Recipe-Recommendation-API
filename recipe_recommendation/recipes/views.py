from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Recipe, Ingredient,UserProfile
from .serializers import RecipeSerializer,IngredientSerializer,SaveRecipeSerializer
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
    

class SaveRecipeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SaveRecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe_id = serializer.validated_data['recipe_id']
            recipe = Recipe.objects.get(id=recipe_id)

            # Get the user's profile
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

            # Add the recipe to favorites
            user_profile.saved_recipes.add(recipe)

            return Response({"message": "Recipe saved to favorites."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        serializer = SaveRecipeSerializer(data=request.data)
        if serializer.is_valid():
            recipe_id = serializer.validated_data['recipe_id']
            recipe = Recipe.objects.get(id=recipe_id)

            # Get the user's profile
            user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

            # Remove the recipe from favorites
            user_profile.saved_recipes.remove(recipe)

            return Response({"message": "Recipe removed from favorites."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ListSavedRecipesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
        saved_recipes = user_profile.saved_recipes.all()
        serializer = RecipeSerializer(saved_recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)    

# --- Ingredient Management Views ---
class IngredientListView(generics.ListCreateAPIView):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer    



# --- Recommendation Views ---
class TopRecipesView(APIView):
    def get(self, request):
        top_recipes = Recipe.objects.order_by('-rating')[:10]
        serializer = RecipeSerializer(top_recipes, many=True)
        return Response(serializer.data)    



# --- Feedback Views ---
class RecipeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        recipe = Recipe.objects.filter(id=pk).first()
        if not recipe:
            return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)

        rating = request.data.get('rating')
        comment = request.data.get('comment')

        recipe.feedback.create(user=request.user, rating=rating, comment=comment)
        return Response({"message": "Feedback added successfully."})