import math

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

from meal.models import UserFoodEntry

MINIMUM_DAILY_CALORIES = 1200
KG_TO_CAL_RATIO = 7716


class Profile(models.Model):
    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('health', 'Healthier Lifestyle'),
        ('anxiety', 'Manage Anxiety'),
    ]

    ACTIVITY_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Lightly active (light exercise 1-3 days a week)'),
        ('moderate', 'Moderately active (moderate exercise 3-5 days a week)'),
        ('active', 'Active (hard exercise 6-7 days a week)'),
        ('very_active', 'Very active (very hard exercise/sports & physical job)'),
    ]

    SEX_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other')]

    name = models.CharField(max_length=100, default='Default Name')
    goal = models.CharField(max_length=50, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=100, choices=ACTIVITY_CHOICES)
    sex = models.CharField(max_length=10, choices=SEX_CHOICES)
    weight = models.IntegerField()
    goal_weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    weekly_weight_gain_or_loss_goal = models.FloatField(default=0.5)

    def __str__(self):
        return self.user.username

    @property
    def daily_needed_calories(self):
        weight = self.weight
        goal_weight = self.goal_weight
        height = self.height
        age = self.age
        sex = self.sex
        gain_or_loss_goal = self.weekly_weight_gain_or_loss_goal
        activity_level = self.activity_level

        tdee_factors = {'sedentary': 1.2, 'light': 1.375, 'moderate': 1.55, 'active': 1.725, 'very_active': 1.9}
        factor = tdee_factors[activity_level]

        if sex == 'male':
            bmr = 10 * weight + 6.25 * height - 5 * age + 5
        elif sex == 'female':
            bmr = 10 * weight + 6.25 * height - 5 * age - 161
        else:
            bmr = 10 * weight + 6.25 * height - 5 * age - 78  # average of both
        tdee = math.ceil(bmr * factor)
        if goal_weight < weight:
            weekly_deficit = gain_or_loss_goal * KG_TO_CAL_RATIO
            daily_deficit = math.ceil(weekly_deficit / 7)
            daily_intake = tdee - daily_deficit
            return daily_intake
        if goal_weight > weight:
            weekly_surplus = gain_or_loss_goal * KG_TO_CAL_RATIO
            daily_surplus = math.ceil(weekly_surplus / 7)
            daily_intake = tdee + daily_surplus
            return daily_intake
        else:
            return tdee

    @property
    def weeks_until_goal_reached(self):
        if self.weekly_weight_gain_or_loss_goal == 0 and self.goal not in ['weight_loss', 'muscle_gain']:
            return 0
        elif self.weekly_weight_gain_or_loss_goal == 0 and self.goal in ['weight_loss', 'muscle_gain']:
            self.weekly_weight_gain_or_loss_goal = 0.5
            self.save()
        number_of_weeks_until_goal = abs(math.ceil((self.goal_weight - self.weight) / self.weekly_weight_gain_or_loss_goal))
        return int(number_of_weeks_until_goal)

    @property
    def calorie_warning(self):
        if self.daily_needed_calories < MINIMUM_DAILY_CALORIES:
            return True
        return False


class WeightHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.IntegerField()
    date_logged = models.DateField(default=date.today)

    def __str__(self):
        return f"Weight: {self.weight}, Date: {self.date_logged}"



