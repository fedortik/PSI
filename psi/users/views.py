import base64

import djoser
import requests
from django.core.mail import send_mail
from django.db.models import Count, F, Max
from rest_framework import generics, status, pagination, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from . import tests
from .serializers import *

class TokenValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'psychologist'):
            return Response({'role': 'psychologist', 'access': 'True'}, status=status.HTTP_200_OK)
        elif hasattr(user, 'assistant'):
            return Response({'role': 'assistant', 'access': user.assistant.access}, status=status.HTTP_200_OK)
        else:
            return Response({'role': 'unknown'}, status=status.HTTP_200_OK)


class RegistrationView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user_data = serializer.validated_data
            user = User.objects.create_user(**user_data)
            Psychologist.objects.create(user=user)
            return Response({'message': 'The user has been successfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if not hasattr(user, 'psychologist'):
            return Response({'error': 'You are not a psychologist'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserCreateSerializer(data=request.data)

        if serializer.is_valid():
            user_data = serializer.validated_data
            assistant_user = User.objects.create_user(**user_data)
            Assistant.objects.create(user=assistant_user, psychologist=user.psychologist, access=False)
            return Response({'message': 'The assistant has been successfully created'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        assistant_id = request.query_params.get('assistant_id')
        user = request.user

        if not hasattr(user, 'psychologist'):
            return Response({'error': 'You are not a psychologist'}, status=status.HTTP_403_FORBIDDEN)

        try:
            assistant = get_object_or_404(Assistant, id=assistant_id)

            if user.psychologist != assistant.psychologist:
                return Response({'error': 'you have no rights'}, status=status.HTTP_403_FORBIDDEN)

            assistant.user.delete()

            return Response({'message': 'The assistant was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Assistant.DoesNotExist:
            return Response({"message": "Assistant not found"}, status=status.HTTP_404_NOT_FOUND)


class MyAssistantsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AssistantSerializer

    def get_queryset(self):
        user = self.request.user
        if not hasattr(user, 'psychologist'):
            return Response({'error': 'You are not a psychologist'}, status=status.HTTP_403_FORBIDDEN)
        return Assistant.objects.filter(psychologist=user.psychologist)


class GetMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreatePatientView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = self.request.user
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        psychologist = None
        if user.psychologist:
            psychologist = user.psychologist
        elif user.assistant:
            psychologist = user.assistant.psychologist
        serializer.save(psychologist=psychologist)
        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
    template = None


class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['last_name', 'first_name']
    pagination_class = CustomPagination

    def get_queryset(self):
        user = self.request.user
        queryset = Patient.objects.all()

        if hasattr(user, 'psychologist'):
            queryset = queryset.filter(psychologist=user.psychologist).order_by('id')
        elif hasattr(user, 'assistant'):
            queryset = queryset.filter(psychologist=user.assistant.psychologist).order_by('id')

        # Проверяем параметры запроса и применяем сортировку
        sort = self.request.query_params.get('sort')
        vozrast = self.request.query_params.get('vozrast')

        if sort == 'fio':
            if vozrast:
                queryset = queryset.order_by(F('last_name').desc(nulls_last=True),
                                             F('first_name').desc(nulls_last=True))
            else:
                queryset = queryset.order_by(F('last_name').asc(nulls_last=True),
                                             F('first_name').asc(nulls_last=True))
        elif sort == 'date':

            if vozrast:
                queryset = queryset.annotate(last_test_date=Max('testing__time_update')).order_by(
                    F('last_test_date').desc(nulls_last=True))
            else:
                queryset = queryset.annotate(last_test_date=Max('testing__time_update')).order_by(
                    F('last_test_date').asc(nulls_last=True))

        elif sort == 'count':
            znak = ''
            if not vozrast:
                znak = '-'
            queryset = queryset.annotate(testings_count=Count('testing')).order_by(znak + 'testings_count')

        return queryset


class CreateTestingView(generics.CreateAPIView):
    serializer_class = TestingCreateSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        tests = request.data.get('tests')
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({"message": "Patient_id not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if hasattr(user, 'psychologist'):
            if user.psychologist != patient.psychologist:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
            psychologist = user.psychologist
        elif hasattr(user, 'assistant'):
            if user.assistant.psychologist != patient.psychologist:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
            psychologist = user.assistant.psychologist

        serializer = self.get_serializer(data={'patient': patient_id, 'tests': tests})
        serializer.is_valid(raise_exception=True)
        serializer.save(psychologist=psychologist, is_active=True)

        return Response({"id": serializer.instance.id}, status=status.HTTP_201_CREATED)


class PutPatientView(generics.UpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def put(self, request, *args, **kwargs):
        testing_id = request.data.get('testing_id')

        try:
            testing = Testing.objects.get(id=testing_id, is_active=True)

            patient = testing.patient

            serializer = self.get_serializer(patient, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({"message": "Patient information has been updated successfully"}, status=status.HTTP_200_OK)
        except Testing.DoesNotExist:
            return Response({"message": "Testing was not found or is not active"}, status=status.HTTP_404_NOT_FOUND)


class PutTestingResultView(generics.UpdateAPIView):
    queryset = Testing.objects.all()
    serializer_class = TestingUpdateSerializer

    def put(self, request, *args):
        testing_id = request.data.get('testing_id')
        results = request.data.get('results')
        time_results = request.data.get('time_results')
        results_obr = {}

        for test_name, test_answers in results.items():
            if test_name in tests.test_functions:
                processed_results = tests.test_functions[test_name](test_answers)
                results_obr[test_name] = processed_results


        try:
            testing = Testing.objects.get(id=testing_id, is_active=True)

            serializer = self.get_serializer(testing, data={'results': results,'results_obr': results_obr, 'time_results': time_results,
                                                            'is_active': False}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            msg = f'''Уважаемый(ая) {testing.psychologist.user.email},

{f'{testing.patient.last_name} {testing.patient.first_name}' if testing.patient.last_name or testing.patient.first_name else 'Пациент без'} прошла(ел) тестирование. Результат можно посмотреть здесь: 
psychology-gray.vercel.app/dashboard/{testing.id}

С уважением,
коллектив платформы
Психометрический Скоринг Личности
psyhometric.ru'''

            subject = 'Пройден тест'
            from_email = 'fedortik@gmail.com'
            recipient_list = [testing.psychologist.user.email]

            send_mail(subject, msg, from_email, recipient_list,
                      fail_silently=False,
                      auth_user='fedortik@gmail.com',  # Ваша учетная запись Gmail
                      auth_password='ypie olyu gdas djqx',  # Пароль вашей учетной записи Gmail
                      connection=None)

            return Response({"message": "The test result is saved"}, status=status.HTTP_200_OK)
        except Testing.DoesNotExist:
            return Response({"message": "Testing was not found or is not active"}, status=status.HTTP_404_NOT_FOUND)


class PatientTestingDetailView(APIView):
    serializer_class = TestingViewSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args):
        user = request.user
        testing_id = request.query_params.get('testing_id')

        try:
            testing = Testing.objects.get(id=testing_id)
            patient = testing.patient

        except (Patient.DoesNotExist, Testing.DoesNotExist):
            return Response({'error': 'Patient or testing not found'}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(user, 'psychologist'):
            if user.psychologist != patient.psychologist:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
        elif hasattr(user, 'assistant'):
            if user.assistant.psychologist != patient.psychologist:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
            if not user.assistant.access:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.serializer_class(testing)

        return Response(serializer.data)


class GetTestingView(APIView):
    serializer_class = TestingSerializer

    def get(self, request, *args, **kwargs):
        testing_id = request.query_params.get('testing_id')

        try:
            testing = Testing.objects.get(id=testing_id, is_active=True)
        except Testing.DoesNotExist:
            return Response({'error': 'Тesting was not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(testing)

        return Response(serializer.data)


class AccessUpdateView(generics.UpdateAPIView):
    queryset = Assistant.objects.all()
    serializer_class = AssistantSerializer

    def put(self, request, *args, **kwargs):
        assistant_id = request.data.get('assistant_id')
        access = request.data.get('access')
        user = request.user

        if not hasattr(user, 'psychologist'):
            return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)

        try:
            assistant = Assistant.objects.get(id=assistant_id)

            if user.psychologist != assistant.psychologist:
                return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)

            assistant.access = bool(access)
            assistant.save()

            return Response({"message": "Assistant access has been updated successfully"}, status=status.HTTP_200_OK)
        except Assistant.DoesNotExist:
            return Response({"message": "Assistant was not found"}, status=status.HTTP_404_NOT_FOUND)


class DeletePatientView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        patient_id = request.query_params.get('patient_id')
        user = request.user

        try:
            patient = Patient.objects.get(id=patient_id)

            if hasattr(user, 'psychologist'):
                if user.psychologist != patient.psychologist:
                    return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
            elif hasattr(user, 'assistant'):
                if user.assistant.psychologist != patient.psychologist:
                    return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)
                if not user.assistant.access:
                    return Response({'error': 'You have no rights!'}, status=status.HTTP_403_FORBIDDEN)

            patient.delete()

            return Response({'message': 'The Patient was successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Patient.DoesNotExist:
            return Response({"message": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)



class ConvertBase64ToPDF(APIView):
    def post(self, request):
        try:
            base64_data = request.data.get('base64_data', None)
            if not base64_data:
                return Response({'error': 'base64_data is required'}, status=status.HTTP_400_BAD_REQUEST)
            html_content = base64.b64decode(base64_data).decode('utf-8')

            response = requests.post(
                'https://api.pdfshift.io/v3/convert/pdf',
                auth=('api', 'sk_cf3f2dc09a6de75847b588b90a7299689adbfc8e'),
                json={'source': html_content, 'landscape': True},
            )

            response.raise_for_status()

            response = Response({base64.b64encode(response.content).decode('utf-8')})
            response['Content-Disposition'] = 'attachment; filename="output.pdf"'

            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from  djoser.serializers import PasswordResetConfirmSerializer

print(djoser.serializers.PasswordResetConfirmSerializer)