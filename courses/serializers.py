from rest_framework import serializers
from .models import Category, Course, Lesson, Enrollment, LessonProgress
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher = UserSerializer(read_only=True)
    lessons = LessonSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'

class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonProgress
        fields = '__all__'

class CreateEnrollmentSerializer(serializers.ModelSerializer):
    course_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Enrollment
        fields = ('course_id',)

    def create(self, validated_data):
        course_id = validated_data.pop('course_id')
        student = self.context['request'].user
        course = Course.objects.get(id=course_id)
        enrollment, created = Enrollment.objects.get_or_create(student=student, course=course)
        if created:
            enrollment.save()
        return enrollment