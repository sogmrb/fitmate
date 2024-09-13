from datetime import timedelta

from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.views import View

from user.models import Profile
from .forms import UserExerciseEntryForm, UserExerciseEntryManualForm, ExerciseSearchForm
from .models import UserExerciseEntry, Exercise
from core.mixins import CustomLoginRequiredMixin
from core.helper_functions import total_daily_burned, calculate_burned_calories


class IndexView(CustomLoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            logout(request)
            return redirect("user:my_login")
        selected_date = request.GET.get('date')

        name = profile.name
        if selected_date:
            date = timezone.datetime.strptime(selected_date, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()

        prev_date = (date - timedelta(days=1)).strftime('%Y-%m-%d')
        next_date = (date + timedelta(days=1)).strftime('%Y-%m-%d')

        isToday = False
        if date == timezone.now().date():
            isToday = True


        user_exercise_entries = UserExerciseEntry.objects.filter(user=user, date=date)

        if not user_exercise_entries.exists():
            return render(request, "exercise/index.html",
                          {"message": True, 'date': date, 'prev_date': prev_date,
                           'next_date': next_date, 'name': name, 'burned': 0, 'minutes':0, 'isToday': isToday})

        burned, minutes = total_daily_burned(user_exercise_entries)
        return render(request, "exercise/index.html",
                      {
                          "exercise_entries": user_exercise_entries,
                          'date': date,
                          'prev_date': prev_date,
                          'next_date': next_date,
                          'name': name,
                          'burned': burned,
                          'minutes': minutes,
                          'isToday': isToday
                      })


class AddView(CustomLoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        date = request.GET.get('date', '')
        if date is None:
            date = timezone.now().date()
        form = UserExerciseEntryForm()
        exercise = get_object_or_404(Exercise, pk=pk)
        name = exercise.name

        return render(request, "exercise/add.html", {"form": form, "date": date, "exercise_name": name})

    def post(self, request, pk, *args, **kwargs):
        date = request.GET.get('date')
        if date is None:
            date = timezone.now().date()
        form = UserExerciseEntryForm(request.POST)
        exercise = get_object_or_404(Exercise, pk=pk)
        name = exercise.name
        user = request.user
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = user
            entry.name = name
            entry.date = date
            entry.exercise = exercise
            MET_value = exercise.MET_value
            duration = entry.duration
            profile = Profile.objects.get(user=user)
            weight = profile.weight
            entry.burned_calories = calculate_burned_calories(weight, MET_value, duration)
            entry.save()

            return JsonResponse({"success": True})
        return render(request, "exercise/add.html", {"form": form, "date": date, "exercise_name": name})


class AddManualView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        date = request.GET.get('date')
        if date is None:
            date = timezone.now().date()
        form = UserExerciseEntryManualForm()

        return render(request, "exercise/add_manual.html", {"form": form, "date": date})

    def post(self, request, *args, **kwargs):
        user = request.user
        date = request.GET.get('date')
        if date is None:
            date = timezone.now().date()
        form = UserExerciseEntryManualForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.is_manual = True
            entry.user = user
            entry.date = date
            entry.save()
            return JsonResponse({"success": True})
        return render(request, "exercise/add_manual.html", {"form": form, "date": date})


class SearchView(CustomLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        exercise_query = request.GET.get('query', '')
        date = request.GET.get('date', '')

        if exercise_query:
            query_results = Exercise.objects.filter(name__icontains=exercise_query)
            results = [{'id': exercise.pk, 'name': exercise.name} for exercise in query_results]
            return JsonResponse({"success": True, "results": results})
        return render(request, 'exercise/search.html', {'date': date})


class DetailView(CustomLoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        exercise_entry = get_object_or_404(UserExerciseEntry, pk=pk)
        return render(request, "exercise/detail.html", {"entry": exercise_entry})


class EditView(CustomLoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        exercise_entry = get_object_or_404(UserExerciseEntry, pk=pk)
        if exercise_entry.exercise is None:
            form = UserExerciseEntryManualForm(instance=exercise_entry)
            manual = True
        else:
            form = UserExerciseEntryForm(instance=exercise_entry)
            manual = False

        return render(request, "exercise/edit.html", {'form': form, 'entry': exercise_entry, 'manual': manual})

    def post(self, request, pk, *args, **kwargs):
        exercise_entry = get_object_or_404(UserExerciseEntry, pk=pk)
        if exercise_entry.exercise is None:
            form = UserExerciseEntryManualForm(request.POST, instance=exercise_entry)
            manual = True
        else:
            form = UserExerciseEntryForm(request.POST, instance=exercise_entry)
            manual = False

        if form.is_valid():
            if not manual:
                profile = Profile.objects.get(user=request.user)
                exercise = exercise_entry.exercise
                entry = form.save(commit=False)
                weight = profile.weight
                duration = form.cleaned_data['duration']
                entry.burned_calories = calculate_burned_calories(weight, exercise.MET_value, duration)
                entry.save()

            else:
                form.save()
            return JsonResponse({"success": True})
        return render(request, "exercise/edit.html", {'form': form, 'entry': exercise_entry, 'manual': manual})


class DeleteView(CustomLoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        exercise_entry = get_object_or_404(UserExerciseEntry, pk=pk)
        date = exercise_entry.date.strftime('%Y-%m-%d')
        exercise_entry.delete()
        url = reverse('exercise:index') + f"?date={date}"
        return redirect(url)


