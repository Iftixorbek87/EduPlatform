from django.urls import path
from . import views
from .views import CourseListView

urlpatterns = [
    # Main course list view (shows free + premium courses)
    path('', CourseListView.as_view(), name='course_list'),
    
    # Course detail view
    path('<int:pk>/', views.course_detail_view, name='course_detail'),
    
    # API endpoints
    path('api/courses/', views.api_course_list, name='api_course_list'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('progress/<int:enrollment_id>/<int:lesson_id>/', views.mark_lesson_complete, name='mark_lesson_complete'),
]