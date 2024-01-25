from django import forms
from .models import Course, UserProfile


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Почта')
    message = forms.CharField(label='Текст сообщения', widget=forms.Textarea)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'