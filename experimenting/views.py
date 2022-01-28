import json
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
#WEEK 4 ELIMINAR LINEA DE CODIGO DE CONSOLE.CLEAR EN PROJECTS_LIST.html
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import LoginForm, SignupForm, CreateProjectForm, CreateTicketForm, CreateCommentForm, CreateFileForm
from django.contrib import messages
from .models import Project, Ticket, UserRole, Comment, File, TicketHistory

from django.core.paginator import Paginator

from django.template.loader import render_to_string

from django.views.generic.edit import UpdateView, DeleteView

from django.core import serializers

#AUTH-------------------------------------------------------------------------
def signupView(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
    else:
        form = SignupForm()
    return render(request, "signup.html", {'form': form})
       

def forgotPasswordView(request):
    return render(request, "forgot_password.html")


def adminDashboardView(request):
    return render(request, "admin/dashboard.html")

#PROJECTS----------------------------------------------------------------------

def projectsListView(request):
    search = request.POST.get("search")
    if search: 
        page_obj = get_list_or_404(Project, name__icontains=search)
    else:
        page_obj = Project.objects.all()

    context = {"page_obj": page_obj}

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            template_name="admin/projects_list_logic.html",
            context = {"page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)
       



    return render(request, "admin/projects_list.html", context) 


def projectsDetailView(request, project_id):
    search_user_input = request.POST.get("search_user_input")
    search_ticket_input = request.POST.get("search_ticket_input")
    valor = 0
    project = get_object_or_404(Project, pk=project_id)
    assigned_personnel = project.assigned_personnel.all()
    tickets_list = Ticket.objects.all().filter(project=project)
    if search_user_input:
        assigned_personnel = assigned_personnel.filter(username__icontains=search_user_input)

    if search_ticket_input:
        tickets_list = tickets_list.filter(title__icontains=search_ticket_input)

    context = {
        "assigned_personnel": assigned_personnel,
        "tickets_list": tickets_list,
    }


    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        personnel_html = render_to_string(
            template_name="admin/projects/projects_detail_personnel_logic.html",
            context = {"assigned_personnel": assigned_personnel}
        )

        tickets_html = render_to_string(
            template_name="admin/projects/projects_detail_tickets_logic.html",
            context = {"tickets_list": tickets_list}
        )
        personnel_data_dict = {"personnel_html_from_view": personnel_html}
        tickets_data_dict = {"tickets_html_from_view": tickets_html}

        #The user will 
        if request.headers.get("if-value") == "1":
            return JsonResponse(data=personnel_data_dict, safe=False)
        elif request.headers.get("if-value") == "2":
            return JsonResponse(data=tickets_data_dict, safe=False)
    

    return render(request, "admin/projects_detail.html", context)

def projectsCreateView(request):
    form = CreateProjectForm()
    if request.method == "POST":
        form = CreateProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("projects_create"))
    context = {"form": form}
    return render(request, "admin/projects_create.html", context)

class ProjectsUpdateView(UpdateView):
    model = Project
    fields = ["assigned_personnel", "name", "description"]
    template_name_suffix = "/projects_update_form"

class ProjectsDeleteView(DeleteView):
    template_name_suffix = "/projects_confirm_delete"
    model = Project
    success_url = reverse_lazy("projects_list")


#TICKETS------------------------------------------------------------

def ticketsListView(request):
    search = request.POST.get("search")
    if search: 
        page_obj = get_list_or_404(Ticket, title__icontains=search)
    else:
        page_obj = Ticket.objects.all()

    context = {"page_obj": page_obj}

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        html = render_to_string(
            template_name="admin/tickets/tickets_list_logic.html",
            context = {"page_obj": page_obj}
        )

        data_dict = {"html_from_view": html}

        return JsonResponse(data=data_dict, safe=False)


    return render(request, "admin/tickets/tickets_list.html", context) 

def ticketsCreateView(request):
    form = CreateTicketForm(initial={"submitter": request.user, "modified_by": request.user})
    if request.method == "POST":
        form = CreateTicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("tickets_list"))
    context = {"form": form}
    return render(request, "admin/tickets/tickets_create.html", context)

def ticketsDetailView(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    
    comment_form = CreateCommentForm(initial={"author": request.user, "ticket": ticket})
    file_form = CreateFileForm(initial={"author": request.user, "ticket": ticket})

    if request.method == "POST":
        comment_form = CreateCommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()

    if request.method == "POST":
        file_form = CreateFileForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_form.save()

    comment_list = Comment.objects.filter(ticket=ticket)
    file_list = File.objects.filter(ticket=ticket)
    ticket_history_list = TicketHistory.objects.filter(ticket=ticket)

    context = {
        "ticket": ticket,
        "comment_form": comment_form,
        "comment_list": comment_list,
        "file_form": file_form,
        "file_list": file_list,
        "ticket_history_list": ticket_history_list,
    }

    if request.headers.get("x-requested-with") == "XMLHttpRequest":

        comment_html = render_to_string(
            template_name = "admin/tickets/tickets_detail_comments_logic.html",
            context = {"comment_list": comment_list}
        )
        file_html = render_to_string(
            template_name = "admin/tickets/tickets_detail_files_logic.html",
            context = {"file_list": file_list}
        )

        comment_data_dict = {"comment_html_from_view": comment_html}
        file_data_dict = {"file_html_from_view": file_html}

        if request.headers.get("if-value") == "1":
            return JsonResponse(data=comment_data_dict, safe=False)
        elif request.headers.get("if-value") == "2":
             return JsonResponse(data=file_data_dict, safe=False)
        
    return render(request, "admin/tickets/tickets_detail.html", context)

def ticketUpdateView(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    form = CreateTicketForm(instance=ticket, initial={"modified_by": request.user})

    old_developer = ticket.assigned_developer
    if request.method == "POST":
        form = CreateTicketForm(request.POST or None, instance = ticket)
        if form.is_valid():
            form.save()

            #if the assigned developer was changed, then create a history ticket about it
            new_developer = form.cleaned_data["assigned_developer"]
            if old_developer != new_developer:
                ticket_history = TicketHistory.objects.create(ticket=ticket, old_developer=old_developer, new_developer=new_developer)
        
        

    context = {
        "form": form,
    }
    return render(request, "experimenting/ticket/tickets_update_form.html", context)

class TicketsDeleteView(DeleteView):
    model = Ticket
    template_name_suffix = "/tickets_confirm_delete"
    success_url = reverse_lazy("tickets_list")


def searchProjects(request):
    search = request.GET.get("q")

    if search: 
        page_obj = get_list_or_404(Project, name__icontains=search)
    else:
        page_obj = Project.objects.all()
    
    context = {"page_obj": page_obj}
    
    if request.is_ajax():
        
        html = render_to_string(
            template_name="admin/projects_list_logic.html",
            context = {"page_obj": page_obj}
        )
        
        data_dict = {"html_from_view": html}
        return JsonResponse(data=data_dict, safe=False)
    return render(request, "admin/projects_list.html", context)

    
    projects_list = Project.objects.order_by("-id")[:]
    paginator = Paginator(projects_list, 9)

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {"page_obj": page_obj}
    return render(request, "admin/projects_list.html", context)

def createFileView(request):
    form = CreateFileForm()
    if request.method == "POST":
        form = CreateFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return render(request, "admin/tickets/test.html", {"file_form":form})

#after completing all the views, please try to use the generic views of django; like you did with the forms and views for auth