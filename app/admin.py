from django.contrib import admin
from .models import Course, User


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass
