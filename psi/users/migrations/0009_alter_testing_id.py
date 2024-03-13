# Generated by Django 4.2.9 on 2024-01-17 09:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_alter_testing_results'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testing',
            name='id',
            field=models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]