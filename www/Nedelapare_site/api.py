from django.contrib.auth import login
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import ObjectDoesNotExist
from knox import views as knox_views

from Nedelapare_site.serializers import *
from Nedelapare_site.models import *

from datetime import date, timedelta


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
            'href': f"/wait/?email={serializer.data.get('email', '')}"
        }


    @api_response
    def get(self, request):
        try:
            user = User.objects.get(id=request.data.get('id', -1))
        except ObjectDoesNotExist:
            raise SiteAPIException("Пользователь не найден")
        user.confirmed_email = True
        user.save()
        return {
            'status': 'ОК',
            'href': "/done/"
        }


class Login(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    @api_response
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            raise SiteAPIException('Ошибка авторизации', serializer.errors)
        user = serializer.validated_data['user']
        login(request, user)
        response = super().post(request, format=None)
        return response.data


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_me(request):
    user = request.user
    return Response({
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "position": user.position
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_group(request):
    user = request.user
    if user.position == 0:
        try:
            student = Student.objects.get(user=user.id)
            group = Group.objects.get(id=student.group)
        except ObjectDoesNotExist:
            return Response({
                "error_message": "Группа не найдена"
            }, status=status.HTTP_404_NOT_FOUND)
        university = University.objects.get(id=group.university).name
        faculty = Faculty.objects.get(id=group.faculty).name
        resp = {
            "id": group.id,
            "name": group.name,
            "university": university,
            "faculty": faculty,
            "monday_first_week": group.monday_first_week,
            "start_semester": group.start_semester,
            "end_semester": group.end_semester
        }
        subgroups = list()
        for subgroup in Subgroup.objects.filter(group=group.id):
            subject = Subject.objects.get(id=subgroup.subject)
            flag = True
            for subgroup_in_list in subgroups:
                if subgroup_in_list["subject"] == subject:
                    subgroup_in_list["names"].append({
                        "id": subgroup.id,
                        "name": subgroup.name
                    })
                    flag = False
                    break
            if flag:
                subgroups.append({
                    "subject": subject,
                    "names": [{
                        "id": subgroup.id,
                        "name": subgroup.name
                    }]
                })
        resp.update({
            "subgroups": subgroups
        })
        users_count = 0
        users = list()
        for student in Student.objects.filter(group=group.id):
            user = User.objects.get(id=student.user)
            users.append({
                "name": user.name
            })
            users_count += 1
        resp.update({
            "users_count": users_count,
            "users": users
        })
        return Response(resp, status=status.HTTP_200_OK)
    else:
        return Response({
            "error_message": "Недоступно для преподавателей"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_lessons(request):
    start = request.data.get("start", None)
    end = request.data.get("end", None)
    if start is None or end is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    days_count = (date.fromisoformat(end) - date.fromisoformat(start)).days
    resp = list()
    user = request.user
    if user.position == 0:
        student = Student.objects.get(user=user.id)
        group = Group.objects.get(id=student.group)
        lesson_queryset = Lesson.objects.filter(group=group.id)
    else:
        lesson_queryset = Lesson.objects.filter(teacher_id=user.id)
    for i in range(days_count + 1):
        day = (date.fromisoformat(start) + timedelta(days=i)).isoformat()
        lessons = list()
        for lesson in lesson_queryset.filter(group=group.id, date=day):
            if lesson.subgroup is not None:
                subgroup = Subgroup.objects.get(id=lesson.subgroup)
                subgroup = {
                    "id": subgroup.id,
                    "name": subgroup.name
                }
            else:
                subgroup = None
            lessons.append({
                "id": lesson.id,
                "group": Group.objects.get(id=lesson.group).name,
                "subject": Subject.objects.get(id=lesson.subject).name,
                "subgroup": subgroup,
                "time_start": lesson.time_start,
                "time_end": lesson.time_end,
                "type_of_work": lesson.type_of_work,
                "place": lesson.place
            })
        resp.append({
            "day": day,
            "lessons": lessons
        })
    return Response(resp, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_lesson(request):
    lesson_id = request.data.get("id", None)
    if lesson_id is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    lesson = Lesson.objects.get(id=lesson_id)
    if lesson.subgroup is not None:
        subgroup = Subgroup.objects.get(id=lesson.subgroup)
        subgroup = {
            "id": subgroup.id,
            "name": subgroup.name
        }
    else:
        subgroup = None
    if lesson.teacher_id is not None:
        obj = User.objects.get(id=lesson.teacher_id)
        teacher = {
            "name": obj.name
        }
    else:
        teacher = {
            "name": lesson.teacher_name
        }
    return Response({
        "id": lesson.id,
        "group": Group.objects.get(id=lesson.group).name,
        "subject": Subject.objects.get(id=lesson.subject).name,
        "subgroup": subgroup,
        "date": lesson.date,
        "time_start": lesson.time_start,
        "time_end": lesson.time_end,
        "type_of_work": lesson.type_of_work,
        "place": lesson.place,
        "teacher": teacher,
        "home_work": lesson.home_work
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_name(request):
    instance = User.objects.get(id=request.user.id)
    if request.data.get("name", None) is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data=request.data, instance=instance)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            "error_message": "Недопустимое значение"
        }, status=status.HTTP_400_BAD_REQUEST)
