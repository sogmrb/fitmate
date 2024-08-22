from user.models import User
from django.db import models
from django.utils import timezone


class UserFoodEntry(models.Model):
    food_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    serving_id = models.CharField(max_length=10)
    serving_description = models.CharField(max_length=100)
    serving_choices = models.CharField(max_length=500, default="")
    quantity = models.FloatField(default=1)
    total_calories = models.IntegerField(default=0)
    total_carbs = models.FloatField(default=0)
    total_proteins = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_saturated_fat = models.FloatField(default=0)
    total_polyunsaturated_fat = models.FloatField(default=0)
    total_monounsaturated_fat = models.FloatField(default=0)
    total_cholesterol = models.FloatField(default=0)
    total_sodium = models.FloatField(default=0)
    total_potassium = models.FloatField(default=0)
    total_fibers = models.FloatField(default=0)
    total_sugar = models.FloatField(default=0)
    total_calcium = models.FloatField(default=0)
    total_iron = models.FloatField(default=0)
    total_vitamin_a = models.FloatField(default=0)
    total_vitamin_c = models.FloatField(default=0)

    MEAL_TIME_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('snack', 'Snack'),
    ]
    meal_time = models.CharField(max_length=20, choices=MEAL_TIME_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.food_name}"


class Recipe(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    quantity = models.FloatField()
    UNITS_CHOICES = [
        ('gram', 'gram(s)'),
        ('ml', 'ml(s)'),
        ('serving', 'serving(s)'),
        ('item', 'item(s)')
    ]
    unit = models.CharField(max_length=20, choices=UNITS_CHOICES)
