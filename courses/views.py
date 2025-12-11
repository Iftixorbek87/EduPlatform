from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Course, Category, Enrollment, Progress, Lesson
from .serializers import CourseSerializer, CategorySerializer, EnrollmentSerializer, CreateEnrollmentSerializer, ProgressSerializer
from django.shortcuts import render

@api_view(['GET'])
@permission_classes([AllowAny])
def course_list(request):
    courses = Course.objects.all()
    serializer = CourseSerializer(courses, many=True)
    return Response(serializer.data)

def course_detail_view(request, pk):
    course = Course.objects.get(pk=pk)
    return render(request, 'courses/detail.html', {'course': course})

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
        completed_lessons = enrollment.progress_set.filter(completed_at__isnull=False).count()
        enrollment.progress_percentage = (completed_lessons / total_lessons) * 100 if total_lessons > 0 else 0
        enrollment.save()

        serializer = ProgressSerializer(progress)
        return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)
    except Enrollment.DoesNotExist:
        return Response({'error': 'Ro\'yxatdan o\'tgan kurs topilmadi'}, status=status.HTTP_404_NOT_FOUND)
    except Lesson.DoesNotExist:
        return Response({'error': 'Dars topilmadi'}, status=status.HTTP_404_NOT_FOUND)



from django.utils import timezone  # Bu qatorni views.py boshiga qo'shing