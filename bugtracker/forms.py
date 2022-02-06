from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from .models import Project, Ticket, Comment, File
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from django.forms import ModelMultipleChoiceField, ModelChoiceField

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput)

    username.widget.attrs.update({"class": "form-control", "id": "yourUsername"})
    password.widget.attrs.update({"class": "form-control", "id": "yourPassword"})


class SignupForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget = forms.PasswordInput)
    password2 = forms.CharField(widget = forms.PasswordInput)
    first_name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField()

    first_name.widget.attrs.update({"class": "form-control", "id": "yourName"})
    username.widget.attrs.update({"class": "form-control", "id": "yourUsername"})
    email.widget.attrs.update({"class": "form-control", "id": "yourEmail"})
    password1.widget.attrs.update({"class": "form-control", "id": "yourPassword"})
    password2.widget.attrs.update({"class": "form-control", "id": "yourPassword2"})

    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password1", "password2"]

class PasswordResettingForm(PasswordResetForm):
    email = forms.EmailField()

    email.widget.attrs.update({"class": "form-control", "placeholder": "Email address"})

class PasswordRessetingConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    new_password2 = forms.CharField(max_length=50, widget=forms.PasswordInput)
    
    new_password1.widget.attrs.update({'class': "input100", 'placeholder': 'New Password'})
    new_password2.widget.attrs.update({'class': 'input100', 'placeholder': 'Confirm Password'})

class CreateProjectForm(ModelForm):
    #instead of returning the object name, just return the first_name attribute of the object, in this case User
    class MyModelMultipleChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.first_name

    assigned_personnel = MyModelMultipleChoiceField(queryset=User.objects.all())
    name = forms.CharField(max_length=50)
    description = forms.CharField(max_length=254, widget=forms.Textarea)

    name.widget.attrs.update({"class": "form-control"})
    description.widget.attrs.update({"class": "form-control", "style": "height: 100px"})
    assigned_personnel.widget.attrs.update({"class": "form-select"})

    class Meta:
        model = Project
        fields = ["assigned_personnel", "name", "description"]

class CreateTicketForm(ModelForm):
    class DeveloperModelChoiceField(ModelChoiceField):
        def label_from_instance(self, obj):
            return obj.first_name
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
    assigned_developer = DeveloperModelChoiceField(queryset=User.objects.all())
    project = forms.ModelChoiceField(queryset=Project.objects.all())
    title = forms.CharField(max_length=30)
    description = forms.CharField(max_length=254, widget=forms.Textarea)
    priority_level = forms.ChoiceField(choices=priority_level_choices)
    status = forms.ChoiceField(choices=status_choices)
    ticket_type = forms.ChoiceField(choices=ticket_type_choices)
    
    assigned_developer.widget.attrs.update({"class": "form-select"})
    project.widget.attrs.update({"class": "form-select"})
    title.widget.attrs.update({"class": "form-control"})
    description.widget.attrs.update({"class": "form-control", "style": "height: 100px"})
    priority_level.widget.attrs.update({"class": "form-select"})
    status.widget.attrs.update({"class": "form-select"})
    ticket_type.widget.attrs.update({"class": "form-select"})

    class Meta:
        model = Ticket
        fields = ["submitter", "modified_by", "assigned_developer", "project", "title", "description", "priority_level", "status", "ticket_type"]


class CreateCommentForm(ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    ticket = forms.ModelChoiceField(queryset=Ticket.objects.all())
    description = forms.CharField(max_length=254, widget=forms.Textarea)

    description.widget.attrs.update({"class": "form-control", "style":"height: 100px"})

    class Meta:
        model = Comment
        fields = ["author", "ticket", "description"]

class CreateFileForm(ModelForm):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    ticket = forms.ModelChoiceField(queryset=Ticket.objects.all())
    description = forms.CharField(max_length=254)
    attachment = forms.FileField()

    description.widget.attrs.update({"class": "form-control"})
    attachment.widget.attrs.update({"class": "form-control"})
    

    class Meta:
        model = File
        fields = ["author", "ticket", "description", "attachment"]

class CreateUserRoleForm(forms.Form):
    class UsersModelMultipleChoiceField(ModelMultipleChoiceField):
        def label_from_instance(self, obj):
            return obj.first_name
            
    users = UsersModelMultipleChoiceField(queryset=User.objects.all())
    role = forms.ModelChoiceField(queryset=Group.objects.all())

    users.widget.attrs.update({"class": "form-select"})
    role.widget.attrs.update({"class": "form-select"})

class EditUserRoleForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    groups.widget.attrs.update({"class": "form-select"})

    class Meta:
        model = User
        fields = ["groups"]

class UpdateUserForm(ModelForm):
    username = forms.CharField()
    first_name = forms.CharField(max_length=100, label="Name")
    email = forms.EmailField()
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), required=False)
    is_active = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    is_staff = forms.BooleanField(required=False)

    first_name.widget.attrs.update({"class": "form-control"})
    username.widget.attrs.update({"class": "form-control"})
    email.widget.attrs.update({"class": "form-control"})
    groups.widget.attrs.update({"class": "form-select"})
    is_active.widget.attrs.update({"class": "form-check-input"})
    is_superuser.widget.attrs.update({"class": "form-check-input"})
    is_staff.widget.attrs.update({"class": "form-check-input"})

    class Meta:
        model = User
        fields = ["username", "first_name", "email", "groups", "is_active", "is_superuser", "is_staff"]

class ContactForm(forms.Form):
    user_name = forms.CharField(max_length=60)
    from_email = forms.EmailField()
    subject = forms.CharField(max_length=254)
    message = forms.CharField(widget = forms.Textarea)

    user_name.widget.attrs.update({"class": "form-control", "placeholder": "Your Name"})
    from_email.widget.attrs.update({"class": "form-control", "placeholder": "Your Email"})
    subject.widget.attrs.update({"class": "form-control", "placeholder": "Subject"})
    message.widget.attrs.update({"class": "form-control", "placeholder": "Message", "rows": "6"})
    