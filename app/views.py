from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView

from .forms import CourseForm
from .models import Course, UserProfile


class IndexView(View):
    template_name = 'app/main.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.all()
        return render(request, self.template_name, {'courses': courses})


class CourseDetailView(View):
    template_name = 'app/course_detail.html'

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)


class CourseEditView(View):
    template_name = 'app/edit_course.html'

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = CourseForm(instance=course)
        return render(request, self.template_name, {'form': form, 'course': course})

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Курс успешно отредактирован.')
            return redirect('course_detail', pk=course.pk)
        return render(request, self.template_name, {'form': form, 'course': course})


class CourseDeleteView(View):
    template_name = 'app/del_course.html'

    def get(self, request, pk):
        course = Course.objects.get(pk=pk)
        context = {'course': course}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        course = Course.objects.get(pk=pk)
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


class TeacherListView(ListView):
    template_name = 'app/teachers_list.html'
    model = UserProfile  # Используем UserProfile вместо Teacher
    context_object_name = 'teachers'


class TeacherDetailView(DetailView):
    template_name = 'app/teacher_detail.html'
    model = UserProfile  # Используем UserProfile вместо Teacher
    context_object_name = 'teacher'


@method_decorator(login_required, name='dispatch')
class UserProfileView(View):
    template_name = 'app/profile.html'

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        context = {'user_profile': user_profile, 'authenticated': True}
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class UserProfileEditView(View):
    template_name = 'app/profile_edit.html'

    def get(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user, role=UserProfile.STUDENT)

        form = UserProfileForm(instance=user_profile)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user, role=UserProfile.STUDENT)

        form = UserProfileForm(request.POST, instance=user_profile)

        if form.is_valid():
            form.save()
            return redirect('profile')

        context = {'form': form}
        return render(request, self.template_name, context)


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
