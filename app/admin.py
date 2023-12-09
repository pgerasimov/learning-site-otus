from django.contrib import admin
from .models import Course, Teacher, Student, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    pass
