from django.urls import path

from . import views

app_name = 'user'
urlpatterns = [
    # path("welcome/", views.WelcomeView.as_view(), name="welcome"),
    # path("name/", views.NameView.as_view(), name="name"),
    # path("goals/", views.GoalsView.as_view(), name="goals"),
    # path("activity-level/", views.ActivityLevelView.as_view(), name="activity_level"),
    # path("profile-info/", views.ProfileInfoView.as_view(), name="profile_info"),
    path("welcome/", views.RegisterView.as_view(), name="register"),
    path("login/", views.MyLoginView.as_view(), name="my_login"),
    path("logout/", views.LogoutView.as_view(), name="my_logout"),

]
