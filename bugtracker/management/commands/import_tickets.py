import csv 

from django.core.management import BaseCommand
from django.contrib.auth.models import User

from bugtracker.models import Ticket, Project

class Command(BaseCommand):
    """
    The main purpose of this is to use a fast way to refill
    our database since "I think" we are going to spend
    a lot of time interviewing and I need to show
    my project and tickets with a fresh date

    Command for importing a properly-formated CSV file with ticket
    data into the database.

    #Notes
    Handles creating, TODO: also need to handle updating without "(',')"
    submiter and modified_by fields are referenced to the first user ("who has the id 1")
    assigned_developer field is referenced to the second user
    project field is referenced to the first project

    #CSV Expected format:
    id,title,description,priority_level,status,ticket_type

    
    Close Ticket Functionality,The developer assigned to a specific ticket should 
    be able to close that ticket instead of updating the whole ticket,Low,Open,
    Feature Requests
    """

    def add_arguments(self, parser):
        parser.add_argument("filepath", type=str, help=
            "The path should be like this: path/to/file.csv")

    def handle(self, *args, **options):
        with open(options["filepath"]) as f:
            reader = csv.reader(f)
            user1 = User.objects.get(pk=1)
            user2 = User.objects.get(pk=2)
            project1 = Project.objects.get(pk=1)

            for row in reader:
                if row[0] != "id": #ignore header if exists
                    try:
                        ticket = Ticket.objects.get(pk=row[0])
                        #TODO: update tickets without the output: "(',')"
                        self.stdout.write(self.style.SUCCESS(
                            "Successfully updated ticket: %s" % ticket.id))

                    except Ticket.DoesNotExist:

                        ticket = Ticket.objects.create(
                            id=row[0],
                            submitter=user1,
                            modified_by=user1,
                            assigned_developer=user2,
                            project=project1,
                            title=row[1],
                            description=row[2],
                            priority_level=row[3],
                            status=row[4],
                            ticket_type=row[5],
                        )

                        self.stdout.write(self.style.SUCCESS(
                            "Successfully created ticket: %s" % ticket.id))
                