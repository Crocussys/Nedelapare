from django.urls import path, include

from . import api

urlpatterns = [
    path('auth/', include('knox.urls')),
    path('register', api.Registration.as_view(), name='register'),
]