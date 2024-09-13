from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
]
