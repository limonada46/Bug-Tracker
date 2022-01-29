from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from .models import Project, Ticket, Comment, File
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    username.widget.attrs.update({'class': 'input100', 'placeholder': 'Username'})
    password.widget.attrs.update({'class': 'input100', 'placeholder': 'Password'})

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class PasswordResettingForm(PasswordResetForm):
    email = forms.EmailField()

    email.widget.attrs.update({"class": "form-control", "placeholder": "Email address"})

class PasswordRessetingConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    
    new_password1.widget.attrs.update({'class': "input100", 'placeholder': 'New Password'})
    new_password2.widget.attrs.update({'class': 'input100', 'placeholder': 'Confirm Password'})

class CreateProjectForm(ModelForm):
    assigned_personnel = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=254)

    class Meta:
        model = Project
        fields = ["assigned_personnel", "name", "description"]

class CreateTicketForm(ModelForm):
    priority_level_choices = [
        ("N", "None"),
        ("L", "Low"),
        ("M", "Medium"),
        ("H", "High"),
        ("VH", "Very High"),
    ]

    status_choices = [
        ("NW", "New"),
        ("OP", "Open"),
        ("IP", "In Progress"),
        ("RS", "Resolved"),
        ("AIR", "Additional Info Required"),

    ]

    ticket_type_choices = [
        ("BG", "Bugs/Errors"),
        ("FR", "Feature Requests"),
        ("OC", "Other Comments"),
        ("TDR", "Training / Document Requests"),
    ]
    submitter = forms.ModelChoiceField(queryset=User.objects.all())
    modified_by = forms.ModelChoiceField(queryset=User.objects.all())
    assigned_developer = forms.ModelChoiceField(queryset=User.objects.all())
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=254, widget=forms.Textarea)
    priority_level = forms.ChoiceField(choices=priority_level_choices)
    status = forms.ChoiceField(choices=status_choices)
    ticket_type = forms.ChoiceField(choices=ticket_type_choices)
    

    class Meta:
        model = Ticket
        fields = ["submitter", "modified_by", "assigned_developer", "project", "title", "description", "priority_level", "status", "ticket_type"]


class CreateCommentForm(ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    ticket = forms.ModelChoiceField(queryset=Ticket.objects.all())
    description = forms.CharField(max_length=254, widget=forms.Textarea)

    class Meta:
        model = Comment
        fields = ["author", "ticket", "description"]

class CreateFileForm(ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    ticket = forms.ModelChoiceField(queryset=Ticket.objects.all())
    description = forms.CharField(max_length=254, widget=forms.Textarea)
    attachment = forms.FileField()
    

    class Meta:
        model = File
        fields = ["author", "ticket", "description", "attachment"]

class CreateUserRoleForm(forms.Form):
    users = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    role = forms.ModelChoiceField(queryset=Group.objects.all())

class EditUserRoleForm(ModelForm):
    
    class Meta:
        model = User
        fields = ["groups"]
