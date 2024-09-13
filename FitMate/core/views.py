from datetime import timedelta
from django import forms
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import JsonResponse

from exercise.models import UserExerciseEntry
from user.models import Profile, WeightHistory
from user.forms import ProfileInfoForm
from meal.models import UserFoodEntry
from user.forms import LogWeightForm, WeeklyGainOrLossForm
from core.mixins import CustomLoginRequiredMixin

from core.helper_functions import carb_fat_protein_ratio, total_daily_stats, total_daily_burned, streak_days


class IndexView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return redirect("core:dashboard")


class DashboardView(CustomLoginRequiredMixin, View):

    def get(self, request, log_weight_form=None, weekly_gain_or_loss_form=None, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            logout(request)
            return redirect("user:my_login")

        needed_cals = profile.daily_needed_calories
        total_needed_cals = needed_cals
        carb_in_gram, protein_in_gram, fat_in_gram = carb_fat_protein_ratio(total_needed_cals, profile.goal,
                                                                            profile.activity_level)
        selected_date = request.GET.get('date')

        if selected_date:
            date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()

        prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

        isToday = False
        if date == timezone.now().date():
            isToday = True

        user_food_entries = UserFoodEntry.objects.filter(user=user, date=date).order_by('meal_time')
        eaten_stats = total_daily_stats(user_food_entries)
        eaten_cals = eaten_stats['total_daily_calories']
        eaten_carbs = eaten_stats['total_daily_carbs']
        eaten_proteins = eaten_stats['total_daily_proteins']
        eaten_fats = eaten_stats['total_daily_fats']

        percentage_eaten = round((eaten_cals / total_needed_cals) * 100)
        carb_percentage = round((eaten_carbs / carb_in_gram) * 100)
        protein_percentage = round((eaten_proteins / protein_in_gram) * 100)
        fat_percentage = round((eaten_fats / fat_in_gram) * 100)

        streak_day = streak_days(user, date)

        user_exercise_entries = UserExerciseEntry.objects.filter(user=user, date=date)

        if not user_exercise_entries.exists():
            burned = 0
        else:
            burned,_ = total_daily_burned(user_exercise_entries)

        if log_weight_form is None:
            log_weight_form = LogWeightForm()

        if weekly_gain_or_loss_form is None:
            weekly_gain_or_loss_form = WeeklyGainOrLossForm(instance=profile)

        return render(request, "core/dashboard.html",
                      {"profile": profile,
                       'percentage_eaten': percentage_eaten,
                       'streak_day': streak_day,
                       'date': date,
                       'carb_percentage': carb_percentage,
                       'protein_percentage': protein_percentage,
                       'fat_percentage': fat_percentage,
                       'burned': burned,
                       'log_weight_form': log_weight_form,
                       'weekly_gain_or_loss_form': weekly_gain_or_loss_form,
                       'prev_date': prev_date,
                       'next_date': next_date,
                       'isToday': isToday,
                       })

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        log_weight_form = LogWeightForm(request.POST)
        weekly_gain_or_loss_form = WeeklyGainOrLossForm(request.POST, instance=profile)
        print(request.POST)

        if 'weight' in request.POST:
            if log_weight_form.is_valid():
                if int(log_weight_form.cleaned_data['weight']) < 30:
                    log_weight_form.add_error('weight', forms.ValidationError("Weight cannot be less than 30kg."))
                    return self.get(request, log_weight_form=log_weight_form, *args, **kwargs)
                weight_history = log_weight_form.save(commit=False)
                date = weight_history.date_logged
                today_history = WeightHistory.objects.filter(date_logged=date, profile=profile)
                if today_history:
                    today_history[0].weight = log_weight_form.cleaned_data['weight']
                    today_history[0].save()
                else:
                    weight_history.profile = profile
                    weight_history.save()

                profile.weight = weight_history.weight
                profile.save()

                return redirect('core:dashboard')

            return self.get(request, log_weight_form=log_weight_form, *args, **kwargs)

        if 'weekly_weight_gain_or_loss_goal' in request.POST:
            if weekly_gain_or_loss_form.is_valid():
                print(float(weekly_gain_or_loss_form.cleaned_data['weekly_weight_gain_or_loss_goal']))
                if float(weekly_gain_or_loss_form.cleaned_data['weekly_weight_gain_or_loss_goal']) < 0:
                    weekly_gain_or_loss_form.add_error('weekly_weight_gain_or_loss_goal', forms.ValidationError("Goal value cannot be negative."))
                    return self.get(request, weekly_gain_or_loss_form=weekly_gain_or_loss_form, *args, **kwargs)
                elif float(weekly_gain_or_loss_form.cleaned_data['weekly_weight_gain_or_loss_goal']) > 1:
                    weekly_gain_or_loss_form.add_error('weekly_weight_gain_or_loss_goal',
                                                       forms.ValidationError("Goal value cannot be more than 1kg."))
                    return self.get(request, weekly_gain_or_loss_form=weekly_gain_or_loss_form, *args, **kwargs)
                weekly_gain_or_loss_form.save()
                return redirect('core:dashboard')
            return self.get(request, weekly_gain_or_loss_form=weekly_gain_or_loss_form, *args, **kwargs)

        return self.get(request, log_weight_form=log_weight_form, weekly_gain_or_loss_form=weekly_gain_or_loss_form,*args, **kwargs)


class EditProfileView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        form = ProfileInfoForm(instance=profile)
        if form.errors:
            print(form.errors)
        return render(request, "user/edit_profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(user=request.user)
        old_goal = profile.goal
        form = ProfileInfoForm(request.POST, instance=profile)
        if form.is_valid():
            new_goal = form.cleaned_data['goal']
            new_weight = float(form.cleaned_data['weight'])
            new_goal_weight = float(form.cleaned_data['goal_weight'])

            if new_goal == 'weight_loss' and new_weight <= new_goal_weight:
                form.add_error('goal_weight', forms.ValidationError("If your goal is weight loss, goal weight must be less than current weight"))
            if new_goal == 'muscle_gain' and new_weight >= new_goal_weight:
                form.add_error('goal_weight', forms.ValidationError("If your goal is muscle gain, goal weight must be greater than current weight"))
            if form.errors:
                html = render_to_string("user/edit_profile.html", {"form": form}, request=request)
                return JsonResponse({"success": False, "html": html})

            form.save()
            date = timezone.now().date()
            today_history, created = WeightHistory.objects.get_or_create(
                date_logged=date,
                profile=profile,
                defaults={'weight': form.cleaned_data['weight']}
            )
            if not created:
                today_history.weight = form.cleaned_data['weight']
                today_history.save()

            if new_goal not in ['weight_loss', 'muscle_gain']:
                profile.weekly_weight_gain_or_loss_goal = 0
                profile.save()

            if new_goal in ['weight_loss', 'muscle_gain'] and new_weight != old_goal:
                profile.weekly_weight_gain_or_loss_goal = 0.5
                profile.save()

            return JsonResponse({"success": True})

        html = render_to_string("user/edit_profile.html", {"form": form}, request=request)
        return JsonResponse({"success": False, "html": html})



