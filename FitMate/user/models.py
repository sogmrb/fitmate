from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


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
    daily_needed_calories = models.IntegerField(default=0)
    daily_goal_calories_to_burn = models.IntegerField(default=0)
    weekly_weight_gain_or_loss_goal = models.FloatField(default=0.5)
    days_until_goal_reached = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class WeightHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.IntegerField()
    date_logged = models.DateField(default=timezone.now)



