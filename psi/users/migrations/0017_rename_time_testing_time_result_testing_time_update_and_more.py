# Generated by Django 4.2.9 on 2024-01-21 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_testing_time_testing_time_create_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testing',
            old_name='time',
            new_name='time_result',
        ),
        migrations.AddField(
            model_name='testing',
            name='time_update',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='testing',
            name='time_create',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]