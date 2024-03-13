# Generated by Django 4.2.9 on 2024-01-17 07:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_patients'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patients',
            name='age',
            field=models.CharField(blank=True, max_length=3),
        ),
        migrations.AlterField(
            model_name='patients',
            name='children',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='city_of_birth',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='city_of_residence',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='country_of_birth',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='country_of_residence',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='diseases',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='education',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='gender',
            field=models.CharField(blank=True, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterField(
            model_name='patients',
            name='inn',
            field=models.CharField(blank=True, max_length=12),
        ),
        migrations.AlterField(
            model_name='patients',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='nationality',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='profession',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='patients',
            name='psychologist',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='users.psychologists'),
        ),
    ]