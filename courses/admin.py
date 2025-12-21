from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Course, Lesson, Enrollment, LessonProgress

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_teacher', 'price', 'is_premium', 'is_published', 'created_at')
    list_filter = ('is_premium', 'is_published', 'category', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_premium', 'is_published')
    raw_id_fields = ('teacher',)
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'description', 'category', 'teacher', 'image')
        }),
        ('Narx va holat', {
            'fields': ('price', 'is_premium', 'is_published')
        }),
    )

    def get_teacher(self, obj):
        return obj.teacher.get_full_name() if obj.teacher else "-"
    get_teacher.short_description = 'O\'qituvchi'
    get_teacher.admin_order_field = 'teacher__first_name'

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order', 'notion_url_display')
    list_filter = ('course',)
    search_fields = ('title', 'description', 'notion_url')
    
    def notion_url_display(self, obj):
        if obj.notion_url:
            return format_html('<a href="{}" target="_blank">Notion havolasi</a>', obj.notion_url)
        return "-"
    notion_url_display.short_description = 'Notion Havolasi'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrolled_at')

@admin.register(LessonProgress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('enrollment', 'lesson', 'completed_at')