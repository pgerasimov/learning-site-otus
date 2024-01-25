from django.contrib import admin
from .models import Course, User, UserProfile


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'full_name', 'email', 'age', 'experience', 'workplace', 'bio')
    search_fields = ('user__username', 'full_name', 'email')