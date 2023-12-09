from django.shortcuts import render
from .models import Course


def index(request):
    courses = Course.objects.all()
    return render(request, 'app/main.html', {'courses': courses})


