# Generated by Django 4.0.2 on 2022-02-16 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bugtracker', '0002_alter_comment_description_alter_file_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority_level',
            field=models.CharField(choices=[('none', 'None'), ('low', 'Low'), ('medium', 'Medium'), ('high', 'High'), ('very_high', 'Very High')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='status',
            field=models.CharField(choices=[('new', 'New'), ('open', 'Open'), ('in_progress', 'In Progress'), ('resolved', 'Resolved'), ('additional_info_required', 'Additional Info Required')], max_length=50),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='ticket_type',
            field=models.CharField(choices=[('bugs_errors', 'Bugs/Errors'), ('feature_requests', 'Feature Requests'), ('other_comments', 'Other Comments'), ('training_document_requests', 'Training / Document Requests')], max_length=50),
        ),
    ]
