from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User, Permission

class Project(models.Model):
    assigned_personnel = models.ManyToManyField(User)
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("projects_detail", kwargs={"project_id": self.pk})

class Ticket(models.Model):

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

    submitter = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="submitter", default=1)
    modified_by = models.ForeignKey(User, on_delete=models.RESTRICT, default=1)
    assigned_developer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="assigned_developer", default=1)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField()
    priority_level = models.CharField(max_length=20, choices=priority_level_choices)
    status = models.CharField(max_length=20, choices=status_choices)
    ticket_type = models.CharField(max_length=20, choices=ticket_type_choices)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tickets_list")

   

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    description = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    def __str__(self):
        return self.description

class File(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    description = models.TextField()
    attachment = models.FileField(upload_to="tickets/", blank=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.attachment.url

class TicketHistory(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    old_developer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name="old_dev")
    new_developer = models.ForeignKey(User, on_delete=models.RESTRICT)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.ticket.title

    

