from django.contrib import admin
from Nedelapare_site.models import *

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(University)
admin.site.register(Faculty)
admin.site.register(UniversityToFaculty)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(Subgroup)
admin.site.register(Subject)
admin.site.register(StudentToSubgroup)
admin.site.register(RequestForPositionConfirmation)
