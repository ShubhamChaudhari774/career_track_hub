from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_application_view, name='add_application'),
    path('edit/<int:pk>/', views.edit_application_view, name='edit_application'),
    path('delete/<int:pk>/', views.delete_application_view, name='delete_application'),
    path('detail/<int:pk>/', views.application_detail_view, name='application_detail'),
]
