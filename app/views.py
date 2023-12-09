from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from .models import Course
from django.contrib import messages
from .forms import CourseForm


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
    template_name = 'app/edit_course.html'  # Создайте шаблон для страницы редактирования

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(instance=course)
        return render(request, self.template_name, {'form': form, 'course': course})

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно отредактирован.')
            return redirect('course_detail', pk=course.pk)
        return render(request, self.template_name, {'form': form, 'course': course})


class CourseDeleteView(View):
    template_name = 'app/del_course.html'

    def get(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        messages.success(request, 'Курс успешно удален')
        return redirect('/')


class CourseCreateView(View):
    template_name = 'app/create_course.html'

    def get(self, request):
        form = CourseForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно добавлен')
            return redirect('index')
        return render(request, self.template_name, {'form': form})