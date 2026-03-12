from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from tracker import views as tracker_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Auth
    path('login/',  auth_views.LoginView.as_view(template_name='registration/login.html'),  name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', tracker_views.register_view, name='register'),

    # App
    path('', tracker_views.landing_view, name='landing'),
    path('dashboard/', tracker_views.dashboard_view, name='dashboard'),
    path('applications/', tracker_views.application_list_view, name='application_list'),
    path('applications/add/', tracker_views.application_create_view, name='application_create'),
    path('applications/<int:pk>/edit/', tracker_views.application_update_view, name='application_update'),
    path('applications/<int:pk>/delete/', tracker_views.application_delete_view, name='application_delete'),
    path('applications/<int:pk>/', tracker_views.application_detail_view, name='application_detail'),
    path('search/', tracker_views.search_view, name='search'),
]
