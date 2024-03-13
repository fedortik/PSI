
from django.urls import path, include, re_path
from djoser.views import TokenDestroyView, TokenCreateView, UserViewSet

from .password import CustomUserViewSet
from .views import *


urlpatterns = [
    path('login/', TokenCreateView.as_view()),
    path('logout/', TokenDestroyView.as_view()),
    path('registration/', RegistrationView.as_view()),
    path('token_validation/', TokenValidationView.as_view()),

    path('create_assistant/', CreateAssistantView.as_view()),
    path('delete_assistant/', DeleteAssistantView.as_view()),
    path('my_assistants/', MyAssistantsView.as_view()),
    path('access_update/', AccessUpdateView.as_view()),

    path('get_me/', GetMeView.as_view()),

    path('create_patient/', CreatePatientView.as_view()),
    path('delete_patient/', DeletePatientView.as_view()),
    path('patient_list/', PatientListView.as_view()),
    path('put_patient/', PutPatientView.as_view()),
    path('get_patient_testing/', PatientTestingDetailView.as_view()),
    path('create_testing/', CreateTestingView.as_view()),

    path('get_testing/', GetTestingView.as_view()),
    path('put_testing_results/', PutTestingResultView.as_view()),

    path('generate_pdf/', ConvertBase64ToPDF.as_view()),
    path('password_reset/', CustomUserViewSet.as_view({'post': 'reset_password'})),
    path(r'password_reset_confirm/', UserViewSet.as_view({'post': 'reset_password_confirm'})),333
]
