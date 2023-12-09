from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import LoginView
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.contrib import messages

from .models import Course
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
    template_name = 'app/edit_course.html'

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
        return redirect('index')


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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('/')


class RegisterView(CreateView):
    template_name = 'registration/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Регистрация прошла успешно. Теперь вы можете войти.')
        return response
