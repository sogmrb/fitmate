from django.contrib import admin
from .models import UserFoodEntry, Recipe, RecipeIngredient

admin.site.register(UserFoodEntry)
admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
