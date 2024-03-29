# Generated by Django 4.2.9 on 2024-01-16 18:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_assistant_assistants_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('inn', models.CharField(max_length=12, unique=True)),
                ('country_of_birth', models.CharField(max_length=255)),
                ('city_of_birth', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('country_of_residence', models.CharField(max_length=255)),
                ('city_of_residence', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10)),
                ('age', models.PositiveIntegerField()),
                ('education', models.CharField(max_length=255)),
                ('profession', models.CharField(max_length=255)),
                ('children', models.PositiveIntegerField()),
                ('diseases', models.TextField()),
                ('psychologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.psychologists')),
            ],
        ),
    ]
