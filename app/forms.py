from django import forms
from .models import Course, User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

# Остальной код форм, если есть
