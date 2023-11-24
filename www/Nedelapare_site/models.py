from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The email is not given.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.confirmed_email = False
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('position', 2)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(max_length=254, unique=True)
    confirmed_email = models.BooleanField(default=False)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=256)
    position = models.PositiveSmallIntegerField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'position']

    objects = UserManager()

    def __str__(self):
        return self.name

class Student(models.Model):
    user = models.BigIntegerField()
    group = models.BigIntegerField()

class Teacher(models.Model):
    user = models.BigIntegerField()
    lesson = models.BigIntegerField()

class University(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class Faculty(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name

class UniversityToFaculty(models.Model):
    university = models.BigIntegerField()
    faculty = models.BigIntegerField()

class Group(models.Model):
    university = models.BigIntegerField()
    faculty = models.BigIntegerField()
    name = models.CharField(max_length=32)
    monday_first_week = models.DateField()
    head = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    group = models.BigIntegerField()
    subject = models.CharField(max_length=128)
    date = models.DateField()
    time = models.CharField(max_length=11)
    type_of_work = models.CharField(max_length=32, blank=True)
    place = models.CharField(max_length=32, blank=True)
    teacher_id = models.BigIntegerField(null=True, blank=True)
    teacher_name = models.CharField(max_length=96, blank=True)
    home_work = models.TextField(max_length=512, blank=True)

    def __str__(self):
        return self.subject
