# Generated by Django 4.2.9 on 2024-02-01 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_alter_testing_results'),
    ]

    operations = [
        migrations.AddField(
            model_name='testing',
            name='res',
            field=models.JSONField(blank=True, default=dict),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='testing',
            name='results_obr',
            field=models.JSONField(blank=True, default=dict),
        ),
    ]
