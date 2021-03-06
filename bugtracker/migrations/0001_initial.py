# Generated by Django 4.0 on 2022-01-31 02:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254)),
                ('assigned_personnel', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=254)),
                ('priority_level', models.CharField(choices=[('N', 'None'), ('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('VH', 'Very High')], max_length=20)),
                ('status', models.CharField(choices=[('NW', 'New'), ('OP', 'Open'), ('IP', 'In Progress'), ('RS', 'Resolved'), ('AIR', 'Additional Info Required')], max_length=20)),
                ('ticket_type', models.CharField(choices=[('BG', 'Bugs/Errors'), ('FR', 'Feature Requests'), ('OC', 'Other Comments'), ('TDR', 'Training / Document Requests')], max_length=20)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('assigned_developer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='assigned_developer', to='auth.user')),
                ('modified_by', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, to='auth.user')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.project')),
                ('submitter', models.ForeignKey(default=1, on_delete=django.db.models.deletion.RESTRICT, related_name='submitter', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='TicketHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateField(auto_now_add=True)),
                ('new_developer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='auth.user')),
                ('old_developer', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='old_dev', to='auth.user')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.ticket')),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=254)),
                ('attachment', models.FileField(blank=True, upload_to='tickets/')),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.ticket')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=254)),
                ('created', models.DateField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
                ('ticket', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bugtracker.ticket')),
            ],
        ),
    ]
