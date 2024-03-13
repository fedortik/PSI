from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from djoser.views import UserViewSet
from djoser.conf import settings
from djoser.compat import get_user_email

class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                message="Пароль должен содержать не менее %(min_length)d символов.",
                code='password_too_short',
                params={'min_length': self.min_length},
            )


class CustomAlphanumericValidator:
    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
            raise ValidationError(
                message="Пароль должен содержать как минимум одну цифру и одну букву.",
                code='password_no_digits_or_letters',
            )




class CustomUserViewSet(UserViewSet):
    def reset_password(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user()

        if user:
            context = {"user": user}
            to = [get_user_email(user)]
            settings.EMAIL.password_reset(self.request, context).send(to)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"detail": "User not found with the provided email"}, status=status.HTTP_400_BAD_REQUEST)