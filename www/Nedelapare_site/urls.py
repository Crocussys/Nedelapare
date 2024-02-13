from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signin/', views.sign_in, name='signin'),
    path('reg/', views.registration, name='reg'),
    path('wait/', views.waiting, name='wait'),
    path('done/', views.done_reg, name='done'),
    path('schedule/', views.schedule, name='schedule'),
    path('add/', views.add, name='add'),
    path('profile/', views.profile, name='profile'),
    path('group/', views.group, name='group'),
    path('group_change/', views.group_change, name='group_change'),
    path('test/', views.test, name='test')
]
