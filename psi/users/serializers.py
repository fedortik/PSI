from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *
from django.contrib.auth.models import User
from djoser.serializers import UserCreateSerializer


class UserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        validate_password(value)
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']


class PsychologistSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Psychologist
        fields = '__all__'


class AssistantSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Assistant
        fields = ['id', 'username', 'first_name', 'last_name', 'psychologist', 'access', 'email']


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('psychologist',)


class TestingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = '__all__'
        read_only_fields = ('psychologist',)


class TestingSerializer(serializers.ModelSerializer):
    patient_info = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Testing
        fields = ['id', 'patient_info', 'tests', 'time_update']
        read_only_fields = ('psychologist',)


class TestingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = ['results', 'time_results', 'results_obr']

    def update(self, instance, validated_data):
        instance.results = validated_data['results']
        instance.results_obr = validated_data['results_obr']
        instance.time_results = validated_data['time_results']
        instance.is_active = False
        instance.save()
        return instance


class TestingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testing
        fields = ['id', 'time_create', 'is_active', 'time_update']
        read_only_fields = ('psychologist',)


class PatientListSerializer(serializers.ModelSerializer):
    testings = TestingListSerializer(many=True, read_only=True, source='testing_set')

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ('psychologist',)


class TestingViewSerializer(serializers.ModelSerializer):
    patient_info = PatientSerializer(source='patient', read_only=True)

    class Meta:
        model = Testing
        fields = '__all__'
        read_only_fields = ('psychologist',)

