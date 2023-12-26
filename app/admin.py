from django.contrib import admin
from .models import Course, User, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
