from django.contrib import admin
from .models import Project, Ticket, Role, Comment, File, UserRole, TicketHistory

class TicketAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.modified_by = request.user
        if not change or not obj.submitter:# if nobody has modified it or the submitter does not exist:
            obj.submitter = request.user
        super().save_model(request, obj, form, change)

class CommentAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class FileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Project)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(Role)
admin.site.register(Comment, CommentAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(UserRole)
admin.site.register(TicketHistory)
