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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", auth_views.LoginView.as_view(authentication_form = LoginForm), name="login"),
    path("signup/", views.signupView, name="signup"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path("password_reset/", auth_views.PasswordResetView.as_view(form_class = PasswordResettingForm), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(form_class = PasswordRessetingConfirmForm), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
    path("dashboard/", views.adminDashboardView, name="bugtracker_dashboard"),

    path("my-projects/", views.projectListView, name="project_list"),
    path("my-projects/<int:project_id>/", views.projectDetailView, name="project_detail"),
    path("my-projects/create", views.projectCreateView, name="project_create"),
    path("my-projects/<int:project_id>/edit", views.projectUpdateView, name="project_update"),
    path("my-projects/<int:project_id>/delete", views.projectDeleteView, name="project_delete"),

    path("my-tickets/", views.ticketListView, name="ticket_list"),
    path("my-tickets/<int:ticket_id>/", views.ticketDetailView, name="ticket_detail"),
    path("my-tickets/create/", views.ticketCreateView, name="ticket_create"),
    path("my-tickets/<int:ticket_id>/edit", views.ticketUpdateView, name="ticket_update"),
    path("my-tickets/<int:ticket_id>/delete", views.ticketDeleteView, name="ticket_delete"),

    path("role_assignment/", views.roleAssignmentView, name="role_assignment"),
    path("role_assignment/<int:user_id>/edit", views.roleAssignmentUpdateView, name="role_assignment_update"),

    path("users/", views.userListView, name="user_list"),
    path("users/<int:user_id>/edit", views.userUpdateView, name="user_update"),
    path("users/<int:user_id>/delete", views.userDeleteView, name="user_delete"),

    path("about/", views.aboutView, name="about"),
    path("contact/", views.contactView, name="contact"),
    path("contact/thanks", views.contactThanksView, name="contact_thanks"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

