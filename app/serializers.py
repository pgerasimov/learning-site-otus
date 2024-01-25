from rest_framework import serializers
from django.contrib.auth.models import User

from app.models import Course, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('id', 'user', 'role', 'bio', 'photo', 'full_name', 'email', 'age', 'experience', 'workplace')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'