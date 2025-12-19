# from django.db import models
# from django.conf import settings
# from accounts.models import User
#
# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(blank=True)
#
#     def __str__(self):
#         return self.name
#
# class Course(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     teacher = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
#     created_at = models.DateTimeField(auto_now_add=True)
#     image = models.ImageField(upload_to='courses/', blank=True)
#
#     def __str__(self):
#         return self.title
#
# class Lesson(models.Model):
#     title = models.CharField(max_length=200)
#     video_url = models.URLField(blank=True)
#     content = models.TextField()
#     course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
#     order = models.PositiveIntegerField(default=0)
#     duration = models.IntegerField(default=0)  # daqiqada
#
#     class Meta:
#         ordering = ['order']
#
#     def __str__(self):
#         return f"{self.course.title} - {self.title}"
#
# class Enrollment(models.Model):
#     student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
#     course = models.ForeignKey(Course, on_delete=models.CASCADE)
#     enrolled_at = models.DateTimeField(auto_now_add=True)
#     completed = models.BooleanField(default=False)
#
#     class Meta:
#         unique_together = ('student', 'course')
#
# class Progress(models.Model):
#     enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
#     lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     progress_percentage = models.IntegerField(default=0)









from django.db import models
from django.conf import settings
from accounts.models import User



class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},
        related_name='teaching_courses'
    )
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)
    is_premium = models.BooleanField(
        default=True,
        help_text="Agar belgilansa, kurs pullik bo'ladi. Aksi holda, bepul kurs sifatida ko'rsatiladi."
    )

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    # 🔥 Kinescope video ID (URL yoki faqat ID kiritish mumkin)
    video_id = models.CharField(
        max_length=100,
        help_text="Kinescope video ID yoki URL (masalan: 4h7Nr6fWxutco8HX71Nhiy yoki https://kinescope.io/4h7Nr6fWxutco8HX71Nhiy)",
        blank=True,
        null=True
    )
    
    def clean_video_id(self, video_id):
        """Clean and validate the video ID."""
        if not video_id:
            return None
            
        # Remove any URL parts if a full URL was pasted
        if 'kinescope.io' in video_id:
            video_id = video_id.split('/')[-1].split('?')[0]
            
        # Remove any whitespace or special characters
        import re
        video_id = re.sub(r'[^a-zA-Z0-9]', '', video_id)
        
        # Kinescope IDs are typically 22 characters long
        if len(video_id) != 22:
            print(f"Warning: Video ID '{video_id}' doesn't look like a standard Kinescope ID")
            
        return video_id
        
    def save(self, *args, **kwargs):
        if self.video_id:
            self.video_id = self.clean_video_id(self.video_id)
        
        super().save(*args, **kwargs)
        print(f"Saved video_id: {self.video_id}")  # Debug print

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    order = models.PositiveIntegerField(default=0)
    duration = models.PositiveIntegerField(
        default=0,
        help_text="Dars davomiyligi (daqiqada)"
    )
    is_free = models.BooleanField(
        default=False,
        help_text="Bepul preview darsmi?"
    )

    class Meta:
        ordering = ['order']
        unique_together = ('course', 'order')

    def __str__(self):
        return f"{self.course.title} | {self.order}. {self.title}"


class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},
        related_name='enrollments'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student} → {self.course}"


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='lesson_progress'
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='progress'
    )
    progress_percentage = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    last_watched_second = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('enrollment', 'lesson')

    def __str__(self):
        return f"{self.enrollment.student} - {self.lesson}"
