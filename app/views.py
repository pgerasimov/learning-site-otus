from django.views import View
from django.shortcuts import render, get_object_or_404
from .models import Course


class IndexView(View):
    template_name = 'app/main.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})


class CourseDetailView(View):
    template_name = 'app/course_detail.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)


class CourseEditView(View):
    template_name = 'app/edit_course.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)


class CourseDeleteView(View):
    template_name = 'app/del_course.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)
