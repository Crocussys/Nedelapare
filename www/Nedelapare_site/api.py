from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import ObjectDoesNotExist

from Nedelapare_site.serializers import *
from Nedelapare_site.models import *

class SiteAPIException(Exception):
    def __init__(self, message):
        self.message = message

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
                "error_message": e.message
            }, status=status.HTTP_400_BAD_REQUEST)
        except APIException as e:
            raise e
    return wrapper

class Registration(APIView):
    permission_classes = (AllowAny,)

    @api_response
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            raise SiteAPIException(e.detail)
        serializer.save()

    @api_response
    def get(self, request):
        try:
            user = User.objects.get(email=request.data.get('email', ''))
        except ObjectDoesNotExist as e:
            raise SiteAPIException("Пользователь не найден")
        user.confirmed_email = True
        user.save()
        return {
            'status': 'ОК',
            'href': "#"
        }