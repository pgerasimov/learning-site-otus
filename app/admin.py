from django.contrib import admin
from .models import Course, Teacher, Student, Schedule


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # Настройки для модели Course, если необходимо
    pass


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    # Настройки для модели Teacher, если необходимо
    pass


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    # Настройки для модели Student, если необходимо
    pass


@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    # Настройки для модели Schedule, если необходимо
    pass
