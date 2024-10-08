from django.urls import path
from . import views

app_name = 'exercise'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('add/', views.AddManualView.as_view(), name='add_manual'),
    path('add/<int:pk>/', views.AddView.as_view(), name='add'),
    path('detail/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('edit/<int:pk>/', views.EditView.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeleteView.as_view(), name='delete'),
    path('search/', views.SearchView.as_view(), name='search'),


]