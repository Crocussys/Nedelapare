from django.contrib.postgres.fields import ArrayField
from django.db import models

class User(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=64)
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)
    permission = models.PositiveSmallIntegerField(default=0)

class Student(models.Model):
    user = models.UUIDField(primary_key=True)
    group = models.UUIDField()

class Teachers(models.Model):
    user = models.UUIDField(primary_key=True)
    groups = ArrayField(models.UUIDField())

class University(models.Model):
    name = models.CharField(max_length=128)
    faculties = ArrayField(models.UUIDField())

class Faculty(models.Model):
    name = models.CharField(max_length=128)

class Group(models.Model):
    university = models.UUIDField()
    faculty = models.UUIDField()
    name = models.CharField(max_length=32)
    lessons = ArrayField(models.UUIDField())
    students = ArrayField(models.UUIDField())
    monday_first_week = models.DateField()
    headman = models.UUIDField(blank=True)

class Lessons(models.Model):
    subject = models.CharField(max_length=128)
    time = models.CharField(max_length=11)
    day_of_week = models.PositiveSmallIntegerField()
    week_numbers = ArrayField(models.PositiveSmallIntegerField())
    type_of_work = models.CharField(max_length=32, blank=True)
    place = models.CharField(max_length=32, blank=True)
    teacher_id = models.UUIDField(blank=True)
    teacher_name = models.CharField(max_length=96, blank=True)
    home_work = models.TextField(max_length=512, blank=True)