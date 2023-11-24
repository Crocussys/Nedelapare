from django.urls import path
from knox.views import LogoutView, LogoutAllView

from . import api

urlpatterns = [
    path('reg/', api.Registration.as_view()),
    path('login/', api.Login.as_view()),
    path('logout/', LogoutView.as_view()),
    path('logout-all/', LogoutAllView.as_view()),
]