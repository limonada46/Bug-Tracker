# Generated by Django 4.0 on 2022-01-28 21:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('experimenting', '0015_alter_tickethistory_options_remove_userrole_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userrole',
            name='users',
        ),
        migrations.AddField(
            model_name='userrole',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
    ]
