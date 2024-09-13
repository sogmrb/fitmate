from user.models import User
from django.db import models
from django.utils import timezone


class UserFoodEntry(models.Model):
    food_name = models.CharField(max_length=100)
    food_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    serving_id = models.CharField(max_length=10)
    serving_description = models.CharField(max_length=100)
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

