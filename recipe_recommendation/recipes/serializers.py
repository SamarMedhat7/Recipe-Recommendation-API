from rest_framework import serializers
from .models import Recipe, Ingredient

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'ingredients', 'steps']

class SaveRecipeSerializer(serializers.Serializer):
    recipe_id = serializers.IntegerField()

    def validate_recipe_id(self, value):
        if not Recipe.objects.filter(id=value).exists():
            raise serializers.ValidationError("Recipe does not exist.")
        return value