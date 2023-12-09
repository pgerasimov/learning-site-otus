from django.urls import path
from .views import IndexView, CourseDetailView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('course_detail/<int:pk>/', CourseDetailView.as_view(), name='course_detail'),
]

