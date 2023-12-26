from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    USER_ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES, default='student')
    bio = models.TextField(blank=True)
    photo = models.URLField(default='https://via.placeholder.com/300', blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    workplace = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.full_name


class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    teachers = models.ManyToManyField(UserProfile, related_name='courses_taught', limit_choices_to={'role': 'teacher'})
    students = models.ManyToManyField(UserProfile, related_name='courses_enrolled', limit_choices_to={'role': 'student'})
    start_date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=0)
    image = models.URLField(default='https://via.placeholder.com/300')

    def __str__(self):
        return self.title


class Schedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.course} - {self.day_of_week} {self.start_time}-{self.end_time}"
