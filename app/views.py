from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin


from .decorators.decorators import admin_required, teacher_required
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

import django_rq
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView, FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.forms import UserCreationForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import CourseForm, ContactForm, UserProfileForm
from .models import Course, UserProfile
from .serializers import UserSerializer


def send_contact_email(sender_email, sender_name, message, recipient):
    smtp_host = 'localhost'
    smtp_port = 1025

    server = smtplib.SMTP(smtp_host, smtp_port)

    subject = 'Новое сообщение от {}'.format(sender_name)
    body = 'Отправитель: {}\nEmail: {}\n\n{}'.format(sender_name, sender_email, message)

    msg = MIMEMultipart()
    msg['From'] = 'Наш сервис <support@our-service-email.ru>'
    msg['To'] = recipient
    msg['Subject'] = Header(subject, 'utf-8').encode()
    msg.attach(MIMEText(body, 'plain'))

    server.send_message(msg)
    server.quit()


class IndexView(View):
    template_name = 'app/main.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.prefetch_related('teachers', 'students').all()
        return render(request, self.template_name, {'courses': courses})


class CourseListView(View):
    template_name = 'app/course_list.html'

    def get(self, request, *args, **kwargs):
        courses = Course.objects.prefetch_related('teachers', 'students').all()
        return render(request, self.template_name, {'courses': courses})


class StudentListView(APIView):
    def get(self, request, *args, **kwargs):
        students = UserProfile.objects.filter(role='student')
        serializer = UserSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TeacherListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        teachers = UserProfile.objects.filter(role='teacher')
        serializer = UserSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CourseDetailView(View):
    template_name = 'app/course_detail.html'

    def get(self, request, pk):
        course = Course.objects.filter(pk=pk).values(
            'id',
            'title',
            'description',
            'start_date',
            'summary',
            'duration',
            'image',
            'teachers__user__username',
        ).first()

        context = {'course': course}
        return render(request, self.template_name, context)


class CourseEditView(LoginRequiredMixin, View):
    template_name = 'app/edit_course.html'

    def get(self, request, pk):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher':
            course = Course.objects.prefetch_related('teachers', 'students').get(pk=pk)
            form = CourseForm(instance=course)
            return render(request, self.template_name, {'form': form, 'course': course})
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")

    def post(self, request, pk):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'teacher':
            course = Course.objects.get(pk=pk)
            form = CourseForm(request.POST, instance=course)
            if form.is_valid():
                form.save()
                messages.success(request, 'Курс успешно отредактирован.')
                return redirect('course_detail', pk=course.pk)
            return render(request, self.template_name, {'form': form, 'course': course})
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")



class CourseDeleteView(LoginRequiredMixin, View):
    template_name = 'app/del_course.html'

    @method_decorator(login_required)
    def get(self, request, pk):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
            course = Course.objects.get(pk=pk)
            context = {'course': course}
            return render(request, self.template_name, context)
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")

    @method_decorator(login_required)
    def post(self, request, pk):
        if hasattr(request.user, 'userprofile') and request.user.userprofile.role == 'admin':
            course = Course.objects.get(pk=pk)
            course.delete()
            messages.success(request, 'Курс успешно удален')
            return redirect('index')
        else:
            return HttpResponseForbidden("У вас нет разрешения на доступ к этой странице")


class CourseCreateView(CreateView):
    template_name = 'app/create_course.html'
    form_class = CourseForm
    success_url = '/index/'  # Укажите здесь правильный URL

    @method_decorator(teacher_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        # Добавим пользователя в преподаватели перед сохранением
        user_profile = self.request.user.userprofile
        form.instance.teachers.add(user_profile)

        messages.success(self.request, 'Курс успешно добавлен')
        return super().form_valid(form)


class TeacherListView(ListView):
    template_name = 'app/teachers_list.html'
    queryset = UserProfile.objects.select_related('user')
    context_object_name = 'teachers'


class TeacherDetailView(DetailView):
    template_name = 'app/teacher_detail.html'
    model = UserProfile
    queryset = UserProfile.objects.select_related('user')
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
            user_profile = UserProfile.objects.get_or_create(user=request.user,
                                                             defaults={'role': UserProfile.STUDENT})[0]
        except UserProfile.DoesNotExist:
            user_profile = UserProfile(user=request.user, role=UserProfile.STUDENT)
            user_profile.save()

        form = UserProfileForm(instance=user_profile)
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get_or_create(user=request.user, defaults={'role': UserProfile.STUDENT})[0]
        except UserProfile.DoesNotExist:
            # В случае, если не удалось создать профиль
            user_profile = UserProfile(user=request.user, role=UserProfile.STUDENT)
            user_profile.save()

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


class ContactView(TemplateView):
    template_name = 'app/contact.html'


class ContactSubmitView(FormView):
    template_name = 'app/contact_submit.html'
    form_class = ContactForm
    success_url = reverse_lazy('contacts')

    def form_valid(self, form):
        # Отправка писем через очередь задач
        queue = django_rq.get_queue('default')

        # Используем введенный в форме адрес электронной почты
        user_email = form.cleaned_data['email']

        # Задача для отправки на адрес из формы
        queue.enqueue(
            send_contact_email,
            user_email,
            form.cleaned_data['name'],
            'Уважаемый {}, мы получили ваше сообщение и скоро ответим.'.format(form.cleaned_data['name']),
            'first@example.com'
        )

        # Задача для отправки на адрес админа
        queue.enqueue(
            send_contact_email,
            user_email,
            form.cleaned_data['name'],
            form.cleaned_data['message'],
            'second@example.com'
        )

        messages.success(self.request, 'Сообщение успешно отправлено!')
        return super().form_valid(form)
