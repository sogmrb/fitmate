from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from user.models import Profile
from .api_service import search_food, get_food_details
from .forms import UserFoodEntryForm, FoodSearchForm
from .models import UserFoodEntry
import ast
from core.helper_functions import carb_fat_protein_ratio, total_daily_stats

class IndexView(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        selected_date = request.GET.get('date')
        profile = get_object_or_404(Profile, user=request.user)
        daily_needed_calories = profile.daily_needed_calories
        carb_in_gram, protein_in_gram, fat_in_gram = carb_fat_protein_ratio(daily_needed_calories, profile.goal,
                                                                            profile.activity_level)
        print(daily_needed_calories)
        name = profile.name
        if selected_date:
            date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()

        next_date = None
        prev_date = None
        if date >= timezone.now().date():
            prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        else:
            prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
            next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

        user_food_entries = UserFoodEntry.objects.filter(user=user, date=date).order_by('meal_time')
        daily_needed_calories = daily_needed_calories
        if not user_food_entries.exists():
            return render(request, "meal/index.html",
                          {"message": "No entries for this day.", 'date': date, 'prev_date': prev_date,
                           'next_date': next_date, 'name': name, 'total_calories': daily_needed_calories,
                           'carb_g': carb_in_gram, 'protein_g': protein_in_gram, 'fat_g': fat_in_gram, })

        daily_stats = total_daily_stats(user_food_entries)
        burned_cals = 0
        daily_needed_calories = daily_needed_calories + burned_cals
        print(daily_stats)
        return render(request, "meal/index.html",
                      {
                          "food_entries": user_food_entries,
                          'date': date,
                          'prev_date': prev_date,
                          'next_date': next_date,
                          'daily_stats': daily_stats,
                          'name': name,
                          'total_calories': daily_needed_calories,
                          'carb_g': carb_in_gram, 'protein_g': protein_in_gram, 'fat_g': fat_in_gram,
                      })


class SearchView(View):
    def get(self, request, *args, **kwargs):
        form = FoodSearchForm(request.GET)
        if form.is_valid():
            food_query = form.cleaned_data['query']
            search_results = search_food(food_query)
            food_name_and_id = search_results.get('foods', {}).get('food', [])
            results = [{'id': str(food['food_id']), 'name': food['food_name']} for food in food_name_and_id]
            return render(request, 'meal/search_results.html', {'form': form, 'results': results})
        return render(request, 'meal/search_food.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = FoodSearchForm()
        return render(request, 'meal/search_food.html', {'form': form})


class AddView(View):
    def get(self, request, food_id, *args, **kwargs):
        food_details = get_food_details(food_id)
        details = food_details.get('food', {})
        food_name = details.get('food_name')
        food_servings = details.get('servings', {}).get('serving', [])
        serving_id_desc = [(serving.get('serving_id'), serving.get('serving_description')) for serving in food_servings]
        date = request.GET.get('date')
        form = UserFoodEntryForm()
        form.fields['serving'].choices = serving_id_desc

        return render(request, "meal/add.html", {"form": form, "food_name": food_name, "date": date})

    def post(self, request, food_id, *args, **kwargs):
        food_details = get_food_details(food_id)
        date = request.GET.get('date')
        details = food_details.get('food', {})
        food_name = details.get('food_name')
        food_servings = details.get('servings', {}).get('serving', [])
        serving_id_desc = [(serving.get('serving_id'), serving.get('serving_description')) for serving in food_servings]

        form = UserFoodEntryForm(request.POST)
        form.fields['serving'].choices = serving_id_desc
        if form.is_valid():
            entry = form.save(commit=False)
            entry.food_name = food_name
            entry.food_id = food_id
            entry.user = request.user
            entry.serving_choices = str(serving_id_desc)
            if date is None:
                date = timezone.now().date()
            entry.date = date
            serving_id = form.cleaned_data['serving']
            quantity = form.cleaned_data['quantity']
            meal_time = form.cleaned_data['meal_time']

            entry.serving_id = serving_id
            entry.quantity = quantity
            entry.meal_time = meal_time

            serving_from_api = None
            for food_serving in food_servings:
                if food_serving['serving_id'] == serving_id:
                    serving_from_api = food_serving
                    break
            if serving_from_api:
                serving_description = serving_from_api['serving_description']
                entry.serving_description = serving_description
                entry.quantity = quantity

                total_calories = int(round(float(serving_from_api['calories']) * quantity))
                total_carbs = round(float(serving_from_api['carbohydrate']) * quantity)
                total_proteins = round(float(serving_from_api['protein']) * quantity)
                total_fats = round(float(serving_from_api['fat']) * quantity)
                total_saturated_fat = round(float(serving_from_api.get('saturated_fat', 0)) * quantity, 3)
                total_polyunsaturated_fat = round(float(serving_from_api.get('polyunsaturated_fat', 0)) * quantity, 3)
                total_monounsaturated_fat = round(float(serving_from_api.get('monounsaturated_fat', 0)) * quantity, 3)
                total_cholesterol = round(float(serving_from_api.get('cholesterol', 0)) * quantity, 3)
                total_sodium = round(float(serving_from_api.get('sodium', 0)) * quantity, 3)
                total_potassium = round(float(serving_from_api.get('potassium', 0)) * quantity, 3)
                total_fibers = round(float(serving_from_api.get('fiber', 0)) * quantity, 3)
                total_sugar = round(float(serving_from_api.get('sugar', 0)) * quantity, 3)
                total_vitamin_a = round(float(serving_from_api.get('vitamin_a', 0)) * quantity, 3)
                total_vitamin_c = round(float(serving_from_api.get('vitamin_c', 0)) * quantity, 3)
                total_calcium = round(float(serving_from_api.get('calcium', 0)) * quantity, 3)
                total_iron = round(float(serving_from_api.get('iron', 0)) * quantity, 3)

                entry.total_calories = total_calories
                entry.total_carbs = total_carbs
                entry.total_proteins = total_proteins
                entry.total_fats = total_fats
                entry.total_saturated_fat = total_saturated_fat
                entry.total_polyunsaturated_fat = total_polyunsaturated_fat
                entry.total_monounsaturated_fat = total_monounsaturated_fat
                entry.total_cholesterol = total_cholesterol
                entry.total_sodium = total_sodium
                entry.total_potassium = total_potassium
                entry.total_fibers = total_fibers
                entry.total_sugar = total_sugar
                entry.total_vitamin_a = total_vitamin_a
                entry.total_vitamin_c = total_vitamin_c
                entry.total_calcium = total_calcium
                entry.total_iron = total_iron

                entry.save()

            url = reverse('meal:index') + f"?date={date}"
            return redirect(url)


class DetailView(View):
    def get(self, request, pk, *args, **kwargs):
        food_entry = get_object_or_404(UserFoodEntry, pk=pk)
        return render(request, "meal/detail.html", {"entry": food_entry})


class EditView(View):
    def get(self, request, pk, *args, **kwargs):
        food_entry = get_object_or_404(UserFoodEntry, pk=pk)
        form = UserFoodEntryForm(instance=food_entry)
        form.fields['serving'].choices = ast.literal_eval(food_entry.serving_choices)
        return render(request, "meal/edit.html", {"form": form, "food_name": food_entry.food_name})

    def post(self, request, pk, *args, **kwargs):
        food_entry = get_object_or_404(UserFoodEntry, pk=pk)
        form = UserFoodEntryForm(request.POST, instance=food_entry)
        form.fields['serving'].choices = ast.literal_eval(food_entry.serving_choices)
        if form.is_valid():
            form.save()

            return redirect("meal:detail", pk=pk)


class DeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        food_entry = get_object_or_404(UserFoodEntry, pk=pk)
        entry_date = food_entry.date.strftime('%Y-%m-%d')
        food_entry.delete()
        url = reverse('meal:index') + f"?date={entry_date}"
        return redirect(url)
