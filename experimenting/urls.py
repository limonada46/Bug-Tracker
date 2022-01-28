"""experimenting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm, PasswordResettingForm, PasswordRessetingConfirmForm

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", auth_views.LoginView.as_view(authentication_form = LoginForm), name="login"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("forgot_password/", views.forgotPasswordView, name="forgot_password"),

    path("password_reset/", auth_views.PasswordResetView.as_view(form_class = PasswordResettingForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class = PasswordRessetingConfirmForm), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path("dashboard/", views.adminDashboardView, name="BugTracker_dashboard"),

    path("my-projects/", views.projectsListView, name="projects_list"),
    path("my-projects/<int:project_id>/", views.projectsDetailView, name="projects_detail"),
    path("my-projects/create", views.projectsCreateView, name="projects_create"),
    path("my-projects/<int:pk>/edit", views.ProjectsUpdateView.as_view(), name="projects_update"),
    path("my-projects/<int:pk>/delete", views.ProjectsDeleteView.as_view(), name="projects_delete"),

    path("my-tickets/", views.ticketsListView, name="tickets_list"),
    path("my-tickets/<int:ticket_id>/", views.ticketsDetailView, name="tickets_detail"),
    path("my-tickets/create/", views.ticketsCreateView, name="tickets_create"),
    path("my-tickets/<int:ticket_id>/edit", views.ticketUpdateView, name="tickets_update"),
    path("my-tickets/<int:pk>/delete", views.TicketsDeleteView.as_view(), name="tickets_delete"),
    path("test/", views.createFileView, name="test"),
]
