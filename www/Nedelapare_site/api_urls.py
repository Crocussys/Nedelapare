from django.urls import path
from knox.views import LogoutView, LogoutAllView

from . import api

urlpatterns = [
    path('reg/', api.Registration.as_view()),
    path('login/', api.Login.as_view()),
    path('isLogin/', api.is_login),
    path('logout/', LogoutView.as_view()),
    path('logoutAll/', LogoutAllView.as_view()),
    path('getMe/', api.get_me),
    path('getGroup/', api.get_group),
    path('getLessons/', api.get_lessons),
    path('getLesson/', api.get_lesson),
    path('getUniversities/', api.get_universities),
    path('getFaculties/', api.get_faculties),
    path('getGroups/', api.get_groups),
    path('setName/', api.set_name),
    path('setGroup/', api.set_group),
    path('addLessons/', api.add_lessons),
    path('changeLessons/', api.change_lessons),
    path('deleteLessons/', api.delete_lessons)
]
