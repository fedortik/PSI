# Generated by Django 4.2.9 on 2024-01-17 11:11

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_testing_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='id',
            field=models.CharField(default=users.models.generate_random_id, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]
