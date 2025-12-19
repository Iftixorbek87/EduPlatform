from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib import messages
from .models import Course, Category, Enrollment, LessonProgress as Progress, Lesson
from .serializers import CourseSerializer, CategorySerializer, EnrollmentSerializer, CreateEnrollmentSerializer, ProgressSerializer
from django.shortcuts import render

from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'
    
    def get_queryset(self):
        # Get all premium courses
        return Course.objects.filter(is_premium=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        premium_courses = list(self.get_queryset().filter(is_premium=True))
        
        # Mark the first course as an example
        if premium_courses:
            premium_courses[0].is_example = True
            
        context['premium_courses'] = premium_courses
        context['free_course'] = Course.objects.filter(is_premium=False).first()
        return context

# API View for mobile apps
@api_view(['GET'])
@permission_classes([AllowAny])
def api_course_list(request):
    free_course = Course.objects.filter(is_premium=False).first()
    premium_courses = Course.objects.filter(is_premium=True)
    
    free_serializer = CourseSerializer(free_course) if free_course else None
    premium_serializer = CourseSerializer(premium_courses, many=True)
    
    return Response({
        'free_course': free_serializer.data if free_serializer else None,
        'premium_courses': premium_serializer.data
    })

from django.shortcuts import get_object_or_404

def course_detail_view(request, pk):
    try:
        course = get_object_or_404(Course, pk=pk)
        
        # If user is not authenticated, show registration prompt
        if not request.user.is_authenticated:
            messages.warning(request, "Kursni ko'rish uchun iltimos, avval ro'yxatdan o'ting yoki tizimga kiring.")
            return render(request, 'courses/detail.html', {
                'course': course,
                'show_auth_message': True
            })
        
        # If user is authenticated but not enrolled in a premium course
        if course.is_premium and not course.enrollments.filter(student=request.user).exists():
            # Check if this is the example course (first premium course)
            first_premium_course = Course.objects.filter(is_premium=True).first()
            if course.id == first_premium_course.id:
                # Allow access to the example course
                return render(request, 'courses/detail.html', {'course': course})
                
            messages.warning(request, "Ushbu kursni ko'rish uchun kursga yozilishingiz kerak.")
            return render(request, 'courses/detail.html', {
                'course': course,
                'show_enroll_message': True
            })
        
        # If user is authenticated and has access to the course
        return render(request, 'courses/detail.html', {'course': course})
    except Exception as e:
        error_msg = f"Xatolik yuz berdi: {str(e)}"
        print(error_msg)  # Console ga xatolikni chiqaramiz
        return render(request, 'courses/error.html', {'error': error_msg})

@api_view(['GET'])
@permission_classes([AllowAny])
def course_detail(request, pk):
    try:
        course = Course.objects.get(pk=pk)
        serializer = CourseSerializer(course)
        return Response(serializer.data)
    except Course.DoesNotExist:
        return Response({'error': 'Kurs topilmadi'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request):
    serializer = CreateEnrollmentSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        enrollment = serializer.save()
        return Response({'message': 'Kursga muvaffaqiyatli yozildingiz!'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_enrollments(request):
    enrollments = Enrollment.objects.filter(student=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_lesson_complete(request, enrollment_id, lesson_id):
    try:
        enrollment = Enrollment.objects.get(id=enrollment_id, student=request.user)
        lesson = Lesson.objects.get(id=lesson_id, course=enrollment.course)
        progress, created = Progress.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        progress.completed_at = timezone.now()
        progress.progress_percentage = 100
        progress.save()

        # Umumiy progress hisoblash
        total_lessons = enrollment.course.lessons.count()
        completed_lessons = enrollment.lesson_progress.filter(completed_at__isnull=False).count()
        enrollment.progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        enrollment.save()

        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Ro\'yxatdan o\'tgan kurs topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    except Lesson.DoesNotExist:
        return Response({'error': 'Dars topilmadi'}, status=status.HTTP_404_NOT_FOUND)



from django.utils import timezone  # Bu qatorni views.py boshiga qo'shing