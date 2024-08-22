from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View

from .forms import ProfileInfoForm, CreateAccountForm, MyLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth

from core.helper_functions import calculate_daily_needed_calories


# class WelcomeView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'user/welcome_page.html')
#
#
# class NameView(View):
#     def get(self, request, *args, **kwargs):
#         form = NameForm()
#         return render(request, 'user/get_name.html',
#                       {'form': form,
#                        })
#
#     def post(self, request, *args, **kwargs):
#         form = NameForm(request.POST)
#         if form.is_valid():
#             request.session['name'] = form.cleaned_data['name']
#             return redirect('user:goals')
#         print(request.session['name'])
#         return render(request, 'user/get_name.html', {'form': form})
#
#
# class GoalsView(View):
#     def get(self, request, *args, **kwargs):
#         form = GoalsForm()
#         return render(request, 'user/goals.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = GoalsForm(request.POST)
#         if form.is_valid():
#             request.session['goal'] = form.cleaned_data['goal']
#             return redirect('user:activity_level')
#         return render(request, 'user/goals.html', {'form': form})
#
#
# class ActivityLevelView(View):
#     def get(self, request, *args, **kwargs):
#         form = ActivityForm()
#         return render(request, 'user/activity_level.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = ActivityForm(request.POST)
#         if form.is_valid():
#             request.session['activity_level'] = form.cleaned_data['activity_level']
#             return redirect('user:profile_info')
#         return render(request, 'user/activity_level.html', {'form': form})
#
#
# class ProfileInfoView(View):
#     def get(self, request, *args, **kwargs):
#         form = ProfileInfoForm()
#         return render(request, 'user/profile_info.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         form = ProfileInfoForm(request.POST)
#         if form.is_valid():
#             request.session['sex'] = form.cleaned_data['sex']
#             request.session['age'] = form.cleaned_data['age']
#             request.session['height'] = form.cleaned_data['height']
#             request.session['weight'] = form.cleaned_data['weight']
#             request.session['goal_weight'] = form.cleaned_data['goal_weight']
#
#             return redirect('user:register')
#         return render(request, 'user/profile_info.html', {'form': form})


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        profile_form = ProfileInfoForm()
        account_form = CreateAccountForm()
        return render(request, 'user/welcome_page.html', {
            'profile_form': profile_form,
            'account_form': account_form
        })

    def post(self, request, *args, **kwargs):
        profile_form = ProfileInfoForm(request.POST)
        account_form = CreateAccountForm(request.POST)
        print(profile_form.is_valid())
        print(account_form.is_valid())
        if profile_form.is_valid() and account_form.is_valid():
            user = account_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.daily_needed_calories, profile.days_until_goal_reached = calculate_daily_needed_calories(profile)

            profile.save()

            login(request, user)

            return redirect('core:dashboard')
        return render(request, 'user/welcome_page.html', {
            'profile_form': profile_form,
            'account_form': account_form
        })


class MyLoginView(View):

    def get(self, request, *args, **kwargs):
        form = MyLoginForm()
        return render(request, 'user/login.html', {"form": form})

    def post(self, request, *args, **kwargs):
        form = MyLoginForm(request, data=request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect("core:dashboard")
            else:
                form.add_error(None, "Invalid username or password")

        return render(request, 'user/login.html', {"form": form})


class LogoutView(View):

    def get(self, request, *args, **kwargs):
        print("Before logout:", request.session.items())
        logout(request)
        print("After logout:", request.session.items())
        return redirect("user:my_login")
