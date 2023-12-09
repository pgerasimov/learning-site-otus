from django.views import View
from django.shortcuts import render
from .models import Course


class IndexView(View):
    template_name = 'app/main.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})


class CourseView(View):
    template_name = 'app/course.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})