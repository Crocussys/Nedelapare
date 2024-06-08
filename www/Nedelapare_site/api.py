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


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_lessons(request):
    user = request.user
    lessons = request.data.get("lessons", None)
    if lessons is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    if user.position == 0:
        student = Student.objects.get(user=user.id)
        group_id = student.group
    elif user.position == 1:
        teacher_id = user.id
        teacher_name = None
    _serializers = list()
    for lesson in lessons:
        if user.position == 0:
            teacher_id = lesson.get("teacher_id", None)
            teacher_name = lesson.get("teacher_name", None)
        elif user.position == 1:
            group_id = lesson.get("group_id", None)
        else:
            group_id = lesson.get("group_id", None)
            teacher_id = lesson.get("teacher_id", None)
            teacher_name = lesson.get("teacher_name", None)
        subject_id = lesson.get("subject_id", None)
        subject_name = lesson.get("subject_name", None)
        _date = lesson.get("date", None)
        time_start = lesson.get("time_start", None)
        time_end = lesson.get("time_end", None)
        type_of_work = lesson.get("type_of_work", "")
        place = lesson.get("place", "")
        if (group_id is None or (subject_id is None and subject_name is None) or _date is None or time_start is None or
                time_end is None or (teacher_id is None and teacher_name is None)):
            return Response({
                "error_message": "Отсутствуют обязательные параметры"
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            return Response({
                "error_message": "Группа не найдена"
            }, status=status.HTTP_404_NOT_FOUND)
        if subject_id is None:
            subjects = Subject.objects.filter(name=subject_name)
            if len(subjects) == 0:
                serializer = SubjectSerializer(data={
                    "name": subject_name
                })
                if serializer.is_valid(raise_exception=False):
                    serializer.save()
                else:
                    return Response({
                        "error_message": "Недопустимое имя предмета"
                    }, status=status.HTTP_400_BAD_REQUEST)
                subject = serializer.instance
            else:
                subject = subjects[0]
        else:
            try:
                subject = Subject.objects.get(id=subject_id)
            except ObjectDoesNotExist:
                return Response({
                    "error_message": "Предмет не найден"
                }, status=status.HTTP_404_NOT_FOUND)
        data = {
            "group": group.id,
            "subject": subject.id,
            "date": _date,
            "time_start": time_start,
            "time_end": time_end,
            "type_of_work": type_of_work,
            "place": place,
            "home_work": None
        }
        if teacher_id is None:
            data.update({"teacher_name": teacher_name})
        else:
            try:
                teacher = Teacher.objects.get(id=teacher_id)
            except ObjectDoesNotExist:
                return Response({
                    "error_message": "Преподаватель не найден"
                }, status=status.HTTP_404_NOT_FOUND)
            data.update({"teacher_id": teacher.id})
        serializer = LessonSerializer(data=data)
        if serializer.is_valid(raise_exception=False):
            _serializers.append(serializer)
        else:
            return Response({
                "error_message": "Недопустимое значение"
            }, status=status.HTTP_400_BAD_REQUEST)
    _serializers.sort(key=lambda x: x.validated_data.get("date"))
    prev = None
    for i in range(len(_serializers)):
        serializer = _serializers[i]
        serializer.validated_data.update({"previous": prev})
        lesson = serializer.save()
        if prev is not None:
            prev_serializer = _serializers[i - 1]
            prev_serializer.validated_data.update({"next": lesson.id})
            prev_serializer.save()
        prev = lesson.id
    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def change_lessons(request):
    user = request.user
    if user.position == 0:
        student = Student.objects.get(user=user.id)
        group_id = student.group
        teacher_id = request.data.get("teacher_id", None)
        teacher_name = request.data.get("teacher_name", None)
    elif user.position == 1:
        group_id = request.data.get("group_id", None)
        teacher_id = user.id
        teacher_name = None
    else:
        group_id = request.data.get("group_id", None)
        teacher_id = request.data.get("teacher_id", None)
        teacher_name = request.data.get("teacher_name", None)
    others = request.data.get("others", 0)
    _date = request.data.get("date", None)
    lessons_id = request.data.get("id", None)
    subject_id = request.data.get("subject_id", None)
    subject_name = request.data.get("subject_name", None)
    time_start = request.data.get("time_start", None)
    time_end = request.data.get("time_end", None)
    type_of_work = request.data.get("type_of_work", "")
    place = request.data.get("place", "")
    home_work = request.data.get("home_work", None)
    if (lessons_id is None or group_id is None or (subject_id is None and subject_name is None) or
            (others == 0 and _date is None) or time_start is None or time_end is None or
            (teacher_id is None and teacher_name is None)):
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        group = Group.objects.get(id=group_id)
    except ObjectDoesNotExist:
        return Response({
            "error_message": "Группа не найдена"
        }, status=status.HTTP_404_NOT_FOUND)
    if subject_id is None:
        subjects = Subject.objects.filter(name=subject_name)
        if len(subjects) == 0:
            serializer = SubjectSerializer(data={
                "name": subject_name
            })
            if serializer.is_valid(raise_exception=False):
                serializer.save()
            else:
                return Response({
                    "error_message": "Недопустимое имя предмета"
                }, status=status.HTTP_400_BAD_REQUEST)
            subject = serializer.instance
        else:
            subject = subjects[0]
    else:
        try:
            subject = Subject.objects.get(id=subject_id)
        except ObjectDoesNotExist:
            return Response({
                "error_message": "Предмет не найден"
            }, status=status.HTTP_404_NOT_FOUND)
    try:
        lesson = Lesson.objects.get(id=lessons_id)
    except ObjectDoesNotExist:
        return Response({
            "error_message": "Занятие не найдено"
        }, status=status.HTTP_404_NOT_FOUND)
    if others != 0:
        _date = lesson.date
    data = {
        "group": group.id,
        "subject": subject.id,
        "date": _date,
        "time_start": time_start,
        "time_end": time_end,
        "type_of_work": type_of_work,
        "place": place,
        "home_work": home_work
    }
    if teacher_id is None:
        data.update({"teacher_name": teacher_name})
    else:
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except ObjectDoesNotExist:
            return Response({
                "error_message": "Преподаватель не найден"
            }, status=status.HTTP_404_NOT_FOUND)
        data.update({"teacher_id": teacher.id})
    serializer = LessonSerializer(lesson, data=data)
    if serializer.is_valid(raise_exception=False):
        data.pop("date")
        data.pop("home_work")
        if others == 0:
            try:
                prev_lesson = Lesson.objects.get(id=lesson.previous)
                prev_data = {"previous": prev_lesson.id}
            except ObjectDoesNotExist:
                prev_lesson = None
                prev_data = {"previous": None}
            try:
                next_lesson = Lesson.objects.get(id=lesson.next)
                next_data = {"next": next_lesson.id}
            except ObjectDoesNotExist:
                next_lesson = None
                next_data = {"next": None}
            if prev_lesson is not None:
                prev_lesson_serializer = LessonSerializer(prev_lesson, data=next_data)
                if prev_lesson_serializer.is_valid(raise_exception=False):
                    prev_lesson_serializer.save()
            if next_lesson is not None:
                next_lesson_serializer = LessonSerializer(next_lesson, data=prev_data)
                if next_lesson_serializer.is_valid(raise_exception=False):
                    next_lesson_serializer.save()
            serializer.validated_data.update({
                "previous": None,
                "next": None
            })
        elif others == 1:
            try:
                prev_lesson = Lesson.objects.get(id=lesson.previous)
                prev_lesson_serializer = LessonSerializer(prev_lesson, data={"next": None})
                if prev_lesson_serializer.is_valid(raise_exception=False):
                    prev_lesson_serializer.save()
            except ObjectDoesNotExist:
                pass
            serializer.validated_data.update({"previous": None})
            next_id = lesson.next
            while next_id is not None:
                try:
                    next_lesson = Lesson.objects.get(id=next_id)
                    next_id = next_lesson.next
                    next_lesson_serializer = LessonSerializer(next_lesson, data=data)
                    if next_lesson_serializer.is_valid(raise_exception=False):
                        next_lesson_serializer.save()
                except ObjectDoesNotExist:
                    next_id = None
        elif others == 2:
            prev_id = lesson.previous
            while prev_id is not None:
                try:
                    prev_lesson = Lesson.objects.get(id=prev_id)
                    prev_id = prev_lesson.previous
                    prev_lesson_serializer = LessonSerializer(prev_lesson, data=data)
                    if prev_lesson_serializer.is_valid(raise_exception=False):
                        prev_lesson_serializer.save()
                except ObjectDoesNotExist:
                    prev_id = None
            next_id = lesson.next
            while next_id is not None:
                try:
                    next_lesson = Lesson.objects.get(id=next_id)
                    next_id = next_lesson.next
                    next_lesson_serializer = LessonSerializer(next_lesson, data=data)
                    if next_lesson_serializer.is_valid(raise_exception=False):
                        next_lesson_serializer.save()
                except ObjectDoesNotExist:
                    next_id = None
        else:
            return Response({
                "error_message": "Недопустимое значение"
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response({
            "error_message": "Недопустимое значение"
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_lessons(request):
    user = request.user
    lessons_id = request.data.get("id", None)
    others = request.data.get("others", 0)
    if lessons_id is None:
        return Response({
            "error_message": "Отсутствуют обязательные параметры"
        }, status=status.HTTP_400_BAD_REQUEST)
    try:
        lesson = Lesson.objects.get(id=lessons_id)
    except ObjectDoesNotExist:
        return Response({
            "error_message": "Занятие не найдено"
        }, status=status.HTTP_404_NOT_FOUND)
    if others == 0:
        try:
            prev_lesson = Lesson.objects.get(id=lesson.previous)
            prev_data = {"previous": prev_lesson.id}
        except ObjectDoesNotExist:
            prev_lesson = None
            prev_data = {"previous": None}
        try:
            next_lesson = Lesson.objects.get(id=lesson.next)
            next_data = {"next": next_lesson.id}
        except ObjectDoesNotExist:
            next_lesson = None
            next_data = {"next": None}
        if prev_lesson is not None:
            prev_lesson_serializer = LessonSerializer(prev_lesson, data=next_data)
            if prev_lesson_serializer.is_valid(raise_exception=False):
                prev_lesson_serializer.save()
        if next_lesson is not None:
            next_lesson_serializer = LessonSerializer(next_lesson, data=prev_data)
            if next_lesson_serializer.is_valid(raise_exception=False):
                next_lesson_serializer.save()
    elif others == 1:
        try:
            prev_lesson = Lesson.objects.get(id=lesson.previous)
            prev_lesson_serializer = LessonSerializer(prev_lesson, data={"next": None})
            if prev_lesson_serializer.is_valid(raise_exception=False):
                prev_lesson_serializer.save()
        except ObjectDoesNotExist:
            pass
        next_id = lesson.next
        while next_id is not None:
            try:
                next_lesson = Lesson.objects.get(id=next_id)
                next_id = next_lesson.next
                next_lesson.delete()
            except ObjectDoesNotExist:
                next_id = None
    elif others == 2:
        prev_id = lesson.previous
        while prev_id is not None:
            try:
                prev_lesson = Lesson.objects.get(id=prev_id)
                prev_id = prev_lesson.previous
                prev_lesson.delete()
            except ObjectDoesNotExist:
                prev_id = None
        next_id = lesson.next
        while next_id is not None:
            try:
                next_lesson = Lesson.objects.get(id=next_id)
                next_id = next_lesson.next
                next_lesson.delete()
            except ObjectDoesNotExist:
                next_id = None
    else:
        return Response({
            "error_message": "Недопустимое значение"
        }, status=status.HTTP_400_BAD_REQUEST)
    lesson.delete()
    return Response(status=status.HTTP_200_OK)
