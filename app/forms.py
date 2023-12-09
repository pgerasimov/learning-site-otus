from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['image', 'title', 'summary', 'description', 'teachers', 'students', 'start_date', 'duration']

