# Generated by Django 4.2.9 on 2024-02-01 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0028_alter_testing_results'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testing',
            name='res',
        ),
    ]
