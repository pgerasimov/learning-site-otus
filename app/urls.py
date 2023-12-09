from django.urls import path
from .views import IndexView, CourseDetailView, CourseEditView, CourseDeleteView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('course_detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
    path('edit_course/<int:pk>/', CourseEditView.as_view(), name='edit_course'),
    path('del_course/<int:pk>/', CourseDeleteView.as_view(), name='del_course'),

]

