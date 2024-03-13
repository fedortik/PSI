import random
import string
import uuid

from django.contrib.auth.models import User
from django.db import models


class Psychologist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Assistant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    access = models.BooleanField()

    def __str__(self):
        return self.user.username


class Patient(models.Model):
    last_name = models.CharField(max_length=255, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    middle_name = models.CharField(max_length=255, blank=True)
    inn = models.CharField(max_length=12, blank=True)
    country_of_birth = models.CharField(max_length=255, blank=True)
    city_of_birth = models.CharField(max_length=255, blank=True)
    nationality = models.CharField(max_length=255, blank=True)
    country_of_residence = models.CharField(max_length=255, blank=True)
    city_of_residence = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    age = models.CharField(max_length=3, blank=True)
    education = models.CharField(max_length=255, blank=True)
    profession = models.CharField(max_length=255, blank=True)
    children = models.CharField(max_length=255, blank=True)
    diseases = models.CharField(max_length=255, blank=True)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)


def generate_random_id(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


class Testing(models.Model):
    id = models.CharField(primary_key=True, max_length=10, default=generate_random_id, unique=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    psychologist = models.ForeignKey(Psychologist, on_delete=models.CASCADE)
    tests = models.JSONField(max_length=255)
    results = models.JSONField(blank=True, null=True)
    results_obr = models.JSONField(blank=True, null=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    time_results = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
