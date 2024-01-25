from django.urls import path, include
from django.contrib.auth import views as auth_views

from mysite import settings
from .views import IndexView, CourseDetailView, CourseEditView, CourseDeleteView, CourseCreateView, CustomLoginView, \
    RegisterView, UserProfileView, UserProfileEditView, TeacherDetailView, \
    ContactView, ContactSubmitView, CourseListView, StudentListView, TeacherListView, TeacherListAPIView

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__', include(debug_toolbar.urls)),
        path('', IndexView.as_view(), name='index'),
        path('course_detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
        path('edit_course/<int:pk>/', CourseEditView.as_view(), name='edit_course'),
        path('del_course/<int:pk>/', CourseDeleteView.as_view(), name='del_course'),
        path('create_course/', CourseCreateView.as_view(), name='create_course'),
        path('teachers_list/', TeacherListView.as_view(), name='teachers_list'),
        path('teacher_detail/<int:pk>/', TeacherDetailView.as_view(), name='teacher_detail'),
        path('login/', CustomLoginView.as_view(), name='login'),
        path('register/', RegisterView.as_view(), name='register'),
        path('logout/', auth_views.LogoutView.as_view(next_page='index'), name='logout'),
        path('profile/', UserProfileView.as_view(), name='profile'),
        path('profile/<str:username>/', UserProfileView.as_view(), name='profile'),
        path('profile/edit/', UserProfileEditView.as_view(), name='profile_edit'),
        path('contacts/', ContactView.as_view(), name='contacts'),
        path('contact_submit/', ContactSubmitView.as_view(), name='contact_submit'),
        path('api/courses/', CourseListView.as_view(), name='course_list_api'),
        path('api/students/', StudentListView.as_view(), name='student_list_api'),
        path('api/teachers/', TeacherListAPIView.as_view(), name='teacher_list_api'),
    ]
