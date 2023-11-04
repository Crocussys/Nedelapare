from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.sign_in, name='signin'),
    path('reg/', views.registration, name='reg'),
    path('schedule/', views.schedule, name='schedule')
]