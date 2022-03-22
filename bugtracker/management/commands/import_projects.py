import csv 

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from bugtracker.models import Project

class Command(BaseCommand):
    """
    The main purpose of this is to use a fast way to refill
    our database since I think we are going to spend
    a lot of time interviewing and I need to show
    my project and projects with a fresh date

    Command for importing a properly-formated CSV file with 'project'
    data into the database.

    #Notes
    Handles creating, TODO: also need to handle updating without "(',')"
    the assigned_personnel manytomanyfield is set to user 1 (who has id=1) and user 2

    #CSV Expected format:
    id,name,description
    1,Bug Tracker,A project that transforms issues or defects from projects to tickets so a development team can address those issues efficiently by assigning tickets to different developers.
    """

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help=
            "The path should be like this: path/to/file.csv")

    def handle(self, *args, **options):
        with open(options["filepath"]) as f:
            reader = csv.reader(f)
            user1 = User.objects.get(pk=1)
            user2 = User.objects.get(pk=2)

            for row in reader:
                if row[0] != "id": #ignore header if exists
                    try:
                        project = Project.objects.get(pk=row[0])
                        #TODO: update project without the output: "(',')"
                        self.stdout.write(self.style.SUCCESS(
                            "Successfully updated project: %s" % project.id))

                    except Project.DoesNotExist:

                        project = Project.objects.create(
                            id=row[0],
                            name=row[1],
                            description=row[2],
                        )

                        project.assigned_personnel.add(user1)
                        project.assigned_personnel.add(user2)  
                        project.save()

                        self.stdout.write(self.style.SUCCESS(
                            "Successfully created project: %s" % project.id))