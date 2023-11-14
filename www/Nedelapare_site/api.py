from django.contrib.auth import login
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import ObjectDoesNotExist
from knox import views as knox_views

from Nedelapare_site.serializers import *
from Nedelapare_site.models import *

class SiteAPIException(Exception):
    def __init__(self, message, detail=None):
        self.message = message
        self.detail = detail

def api_response(func):
    def wrapper(*args, **kwargs):
        try:
            return Response({
                "error": False,
                "response": func(*args, **kwargs)
            }, status=status.HTTP_200_OK)
        except SiteAPIException as e:
            return Response({
                "error": True,
                "error_message": e.message,
                "detail": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            raise e
    return wrapper

class Registration(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except serializers.ValidationError as e:
            raise SiteAPIException("Некорректные данные", e.detail)
        serializer.save()
        # Отправка письма
        return {
            'status': 'ОК',
            'href': "#"
        }

    @api_response
    def get(self, request):
        try:
            user = User.objects.get(email=request.data.get('email', ''))
        except ObjectDoesNotExist:
            raise SiteAPIException("Пользователь не найден")
        user.confirmed_email = True
        user.save()
        return {
            'status': 'ОК',
            'href': "#"
        }

class Login(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    @api_response
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            login(request, user)
            response = super().post(request, format=None)
        else:
            raise SiteAPIException('Ошибка авторизации', serializer.errors)

        return response.data