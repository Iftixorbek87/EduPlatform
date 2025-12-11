from django.urls import path
from . import views

urlpatterns = [
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path('my-enrollments/', views.my_enrollments, name='my_enrollments'),
    path('progress/<int:enrollment_id>/<int:lesson_id>/', views.mark_lesson_complete, name='mark_lesson_complete'),
    path('', views.course_list, name='course_list'),
    path('<int:pk>/', views.course_detail_view, name='course_detail'),

]