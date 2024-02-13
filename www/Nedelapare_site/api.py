from django.contrib.auth import login
from knox.auth import TokenAuthentication
from rest_framework import status
from rest_framework.decorators import authentication_classes, permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import ObjectDoesNotExist
from knox import views as knox_views
from django_email_verification import send_email

from Nedelapare_site.serializers import *
from Nedelapare_site.models import *

from datetime import date, timedelta


class Registration(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = CreateUserSerializer()
        try:
            validated_data, exist_flag = serializer.validate(request.data)
        except serializers.ValidationError as e:
            return Response({
                "error_message": "Некорректные данные",
                "detail": e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        if not exist_flag:
            user = serializer.create(validated_data)
        else:
            user = CustomUser.objects.get(email=validated_data["email"])
        user.is_active = False
        send_email(user, thread=False)
        return Response(status=status.HTTP_200_OK)


class Login(knox_views.LoginView):
    permission_classes = (AllowAny, )
    serializer_class = LoginSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except:
            return Response({
                "error_message": "Ошибка авторизации",
                "detail": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.validated_data['user']
        login(request, user)
        response = super().post(request, format=None)
        return Response(response.data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def is_login(request):
    return Response(status=status.HTTP_200_OK)


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
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)


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
        try:
            student = Student.objects.get(user=user.id)
            group = Group.objects.get(id=student.group)
        except ObjectDoesNotExist:
            return Response({
                "error_message": "Группа не найдена"
            }, status=status.HTTP_404_NOT_FOUND)
        lesson_queryset = Lesson.objects.filter(group=group.id)
    else:
        lesson_queryset = Lesson.objects.filter(teacher_id=user.id)
    for i in range(days_count + 1):
        day = (date.fromisoformat(start) + timedelta(days=i)).isoformat()
        lessons = list()
        for lesson in sorted(lesson_queryset.filter(group=group.id, date=day), key=lambda les: les.time_start):
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
def get_universities(request):
    data = list()
    queryset = University.objects.all()
    for universe in queryset:
        data.append({
            "id": universe.id,
            "name": universe.name
        })
    return Response({
        "data": data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_faculties(request):
    university_id = request.data.get("university_id", None)
    if university_id is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    data = list()
    queryset = UniversityToFaculty.objects.filter(university=university_id)
    for query in queryset:
        faculty = Faculty.objects.get(id=query.faculty)
        data.append({
            "id": faculty.id,
            "name": faculty.name
        })
    return Response({
        "data": data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_groups(request):
    university_id = request.data.get("university_id", None)
    faculty_id = request.data.get("faculty_id", None)
    if university_id is None or faculty_id is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    data = list()
    queryset = Group.objects.filter(university=university_id).filter(faculty=faculty_id)
    for query in queryset:
        data.append({
            "id": query.id,
            "name": query.name
        })
    return Response({
        "data": data
    }, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_name(request):
    user = request.user
    new_name = request.data.get("name", None)
    if new_name is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    serializer = UserSerializer(data={
        "id": user.id,
        "email": user.email,
        "name": new_name,
        "position": user.position
    }, instance=user)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            "error_message": "Недопустимое значение"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def set_group(request):
    user = request.user
    group_id = request.data.get("group_id", None)
    if group_id is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    if user.position != 0:
        return Response({
            "error_message": "Недоступно для преподавателей"
        }, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response({
            "error_message": "Группа не найдена"
        }, status=status.HTTP_404_NOT_FOUND)
    serializer = StudentSerializer(data={
        "user": user.id,
        "group": group.id
    })
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            "error_message": "Недопустимое значение"
        }, status=status.HTTP_400_BAD_REQUEST)
