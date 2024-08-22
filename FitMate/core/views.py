

from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views import View
from user.models import Profile
from meal.models import UserFoodEntry

from core.helper_functions import carb_fat_protein_ratio, total_daily_stats, streak_days


class IndexView(View, LoginRequiredMixin):
    login_url = "/account/login/"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        return render(request, "core/index.html")


class DashboardView(LoginRequiredMixin, View):
    login_url = "/account/login/"
    redirect_field_name = "redirect_to"

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        needed_cals = profile.daily_needed_calories
        total_needed_cals = needed_cals
        carb_in_gram, protein_in_gram, fat_in_gram = carb_fat_protein_ratio(total_needed_cals, profile.goal,
                                                                            profile.activity_level)
        date = timezone.now().date()
        user_food_entries = UserFoodEntry.objects.filter(user=user, date=date).order_by('meal_time')
        eaten_stats = total_daily_stats(user_food_entries)
        eaten_cals = eaten_stats['total_daily_calories']
        eaten_carbs = eaten_stats['total_daily_carbs']
        eaten_proteins = eaten_stats['total_daily_proteins']
        eaten_fats = eaten_stats['total_daily_fats']

        percentage_eaten = round((eaten_cals / total_needed_cals) * 100)
        carb_percentage = round((eaten_carbs/carb_in_gram)*100)
        protein_percentage = round((eaten_proteins/protein_in_gram)*100)
        fat_percentage = round((eaten_fats/fat_in_gram)*100)

        print(carb_percentage)
        print(protein_percentage)
        print(fat_percentage)

        all_user_entries = UserFoodEntry.objects.filter(user=user).order_by('-date')
        streak_day = streak_days(all_user_entries)
        return render(request, "core/dashboard.html",
                      {"profile": profile,
                       'percentage_eaten': percentage_eaten,
                       'streak_day': streak_day,
                       'date': date,
                       'carb_percentage': carb_percentage,
                       'protein_percentage': protein_percentage,
                       'fat_percentage': fat_percentage,

                       })
