from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group

from .forms import LoginForm, SignupForm, CreateProjectForm, CreateTicketForm, CreateCommentForm, CreateFileForm, CreateUserRoleForm, EditUserRoleForm, UpdateUserForm, ContactForm
from .models import Project, Ticket, Comment, File, TicketHistory

from django.core.mail import BadHeaderError, send_mail

from django.contrib.auth.decorators import login_required, permission_required

from django.db.models import Count

#AUTH-------------------------------------------------------------------------
def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {'form': form})
       

def forgotPasswordView(request):
    return render(request, "forgot_password.html")

@login_required
def adminDashboardView(request):

    # Logic to get a total count for every value in priority_level and other choices fields
    priority = {level[0]: 0 for level in Ticket.priority_level_choices}
    queryset = Ticket.objects.values("priority_level").annotate(priority_count=Count("priority_level"))
    for entry in queryset:
        priority.update({entry["priority_level"]: entry["priority_count"]})

    status = {status[0]: 0 for status in Ticket.status_choices}
    queryset = Ticket.objects.values("status").annotate(status_count=Count("status"))
    for entry in queryset:
        status.update({entry["status"]: entry["status_count"]})

    ticket_type = {ticket_type[0]: 0 for ticket_type in Ticket.ticket_type_choices}
    queryset = Ticket.objects.values("ticket_type").annotate(type_count=Count("ticket_type"))
    for entry in queryset:
        ticket_type.update({entry["ticket_type"]: entry["type_count"]})

    context = {
        "priority": priority,
        "status": status,
        "ticket_type": ticket_type,

    }
    return render(request, "admin/dashboard.html", context)

#PROJECTS----------------------------------------------------------------------

@login_required
@permission_required("bugtracker.view_project")
def projectListView(request):
    
    if request.user.has_perm("bugtracker.change_project"):
        project_list = Project.objects.all()
    else:
        project_list = Project.objects.filter(assigned_personnel=request.user)
    context = {"project_list": project_list}
    return render(request, "admin/projects/project_list.html", context) 

@login_required
@permission_required("bugtracker.view_project")
def projectDetailView(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    assigned_personnel = project.assigned_personnel.all()
    ticket_list = Ticket.objects.all().filter(project=project)

    #if the current user is not assigned to this project:
    if request.user not in project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect:
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("project_list"))

    context = {
        "project": project,
        "assigned_personnel": assigned_personnel,
        "ticket_list": ticket_list,
    }

    return render(request, "admin/projects/project_detail.html", context)

@login_required
@permission_required("bugtracker.add_project")
def projectCreateView(request):
    form = CreateProjectForm()
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("project_list"))
    context = {"form": form}
    return render(request, "admin/projects/project_create.html", context)

@login_required
@permission_required("bugtracker.change_project")
def projectUpdateView(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    #if the current user is not assigned to this project:
    if request.user not in project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("project_list"))

    form = CreateProjectForm(instance = project)
    if request.method == "POST":
        form = CreateProjectForm(request.POST or None, instance = project)
        if form.is_valid():
            form.save()
            return redirect(reverse("project_detail", kwargs={"project_id": project_id}))
    context = {"form": form, "project_id": project_id}

    return render(request, "admin/projects/project_update.html", context)

@login_required
@permission_required("bugtracker.delete_project")
def projectDeleteView(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    #if the current user is not assigned to this project:
    if request.user not in project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("project_list"))

    if request.method == "POST":
        project.delete()
        return redirect(reverse("project_list"))
    return redirect(reverse("project_update", kwargs={"project_id": project_id}))


#TICKETS------------------------------------------------------------

@login_required
@permission_required("bugtracker.view_ticket")
def ticketListView(request):
    if request.user.has_perm("bugtracker.change_project"):
        ticket_list = Ticket.objects.all()
    else:
        #Show the tickets from the projects that includes the current user as assigned personnel
        ticket_list = Ticket.objects.filter(project__assigned_personnel=request.user)
    
    context = {"ticket_list": ticket_list}
    return render(request, "admin/tickets/ticket_list.html", context) 

@login_required
@permission_required("bugtracker.view_ticket")
def ticketDetailView(request, ticket_id):
    context = {}
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user not in ticket.project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect:
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("ticket_list"))

    
    if request.user.has_perm("bugtracker.add_comment"):
        comment_form = CreateCommentForm(initial={"author": request.user, "ticket": ticket})

        if (request.method == "POST") and ("comment_submit" in request.POST):
            comment_form = CreateCommentForm(request.POST)
            if comment_form.is_valid():
                comment_form.save()
        context["comment_form"] = comment_form

    if request.user.has_perm("bugtracker.add_file"):
        file_form = CreateFileForm(initial={"author": request.user, "ticket": ticket})
        if (request.method == "POST") and ("file_submit" in request.POST):
            file_form = CreateFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                file_form.save()
        context["file_form"] = file_form
                

    comment_list = Comment.objects.filter(ticket=ticket)
    file_list = File.objects.filter(ticket=ticket)
    ticket_history_list = TicketHistory.objects.filter(ticket=ticket)

    context.update({
        "ticket": ticket,
        "comment_list": comment_list,
        "file_list": file_list,
        "ticket_history_list": ticket_history_list,
    })

    if request.method == "POST":
        return redirect(reverse("ticket_detail", kwargs={"ticket_id": ticket_id}))
        
    return render(request, "admin/tickets/ticket_detail.html", context)

@login_required
@permission_required("bugtracker.add_ticket")
def ticketCreateView(request):
    form = CreateTicketForm(initial={"submitter": request.user, "modified_by": request.user})
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("ticket_list"))
    context = {"form": form}
    return render(request, "admin/tickets/ticket_create.html", context)

@login_required
@permission_required("bugtracker.change_ticket")
def ticketUpdateView(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = CreateTicketForm(instance=ticket, initial={"modified_by": request.user})

    if request.user not in ticket.project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect:
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("ticket_list"))

    old_developer = ticket.assigned_developer
    if request.method == "POST":
        form = CreateTicketForm(request.POST or None, instance = ticket)
        if form.is_valid():
            form.save()

            #if the assigned developer was changed, then create a history ticket about it
            new_developer = form.cleaned_data["assigned_developer"]
            if old_developer != new_developer:
                ticket_history = TicketHistory.objects.create(ticket=ticket, old_developer=old_developer, new_developer=new_developer)
            return redirect(reverse("ticket_list"))
        
        

    context = {
        "form": form,
        "ticket_id": ticket_id,
    }
    return render(request, "admin/tickets/ticket_update.html", context)

@login_required
@permission_required("bugtracker.delete_ticket")
def ticketDeleteView(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user not in ticket.project.assigned_personnel.all():
        #but if the current user is admin, then pass, else redirect:
        if request.user.has_perm("bugtracker.change_project"):
            pass
        else:
            return redirect(reverse("ticket_list"))
  
    if request.method == "POST":
        ticket.delete()
        return redirect(reverse("ticket_list"))
    return redirect(reverse("ticket_update", kwargs={"ticket_id": ticket_id}))

#ROLE ASSIGNMENT -------------------------------------------------------

@login_required
@permission_required("auth.change_user")
def roleAssignmentView(request):
    form = CreateUserRoleForm()
    if request.method == "POST":
        form = CreateUserRoleForm(request.POST)
        if form.is_valid():
            for user in form.cleaned_data["users"]:
                user.groups.add(form.cleaned_data["role"])
                user.save()
    personnel = User.objects.all()
    context = {
        "form": form,
        "personnel": personnel,
    }
    return render(request, "admin/role/role_assignment.html", context)

@login_required
@permission_required("auth.change_user")
def roleAssignmentUpdateView(request, user_id):
    user = get_object_or_404(User, id=user_id)
    form = EditUserRoleForm(instance = user)
    if request.method == "POST":
        form = EditUserRoleForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect(reverse("role_assignment"))
    
    context = {
        "form": form,
        "user": user,
    }
    return render(request, "admin/role/role_assignment_update.html", context)


#USERS -----------------------------------------------------------------

@login_required
@permission_required("auth.view_user")
def userListView(request):
    user_list = get_list_or_404(User)

    context = {"user_list": user_list}

    return render(request, "admin/users/user_list.html", context)

@login_required
@permission_required("auth.change_user")
def userUpdateView(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UpdateUserForm(instance = user)
    if request.method == "POST":
        form = UpdateUserForm(request.POST or None, instance = user)
        if form.is_valid():
            form.save()
            return redirect(reverse("user_list"))
    context = {
        "form": form,
        "user": user, 
    }
    return render(request, "admin/users/user_update.html", context)

@login_required
@permission_required("auth.delete_user")
def userDeleteView(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == "POST":
        user.delete()
        return redirect(reverse("user_list"))
    return redirect(reverse("user_update", kwargs={"user_id": user_id}))

# INFO AND CONTACT PAGES -----------------------------------------------

@login_required
def aboutView(request):
    return render(request, "admin/about_me.html")

@login_required
def contactView(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            message = form.cleaned_data["message"]
            from_email = form.cleaned_data["from_email"]
            if subject and message and from_email:
                try:
                    send_mail(subject, message, from_email, ["wilasalq2@gmail.com"])
                except BadHeaderError:
                    return redirect(reverse("bugtracker_dashboard"))
                return redirect(reverse("contact_thanks"))
    
    context = {"form": form}
    return render(request, "admin/contact.html", context)

@login_required
def contactThanksView(request):
    return render(request, "admin/contact_thanks.html")

#activar las urls // en produccion hay que hacer otra cosa para mostrar los archivos
#4-luego rellenar la base de datos con datos de prueba
#4.5 virtual environment 
#5.-Subir la pagina a algun dominio


#6.- una funcionalidad muy importante para este tipo de projectos es ask for review...
#7 edit comments and files / delete comments and files
#8 an user should not delete other comment of other users
#9 use email instead of username to login 