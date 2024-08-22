
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path('account/', include('user.urls')),
    path('meals/', include('meal.urls')),
    path('exercises/', include('exercise.urls')),


]
