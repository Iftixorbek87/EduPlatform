from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'role', 'is_approved', 'date_joined')
    list_filter = ('role', 'is_approved', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Shaxsiy ma\'lumotlar', {'fields': ('first_name', 'last_name', 'email')}),
        ('Ruxsatlar', {'fields': ('role', 'is_approved', 'is_active', 'is_staff', 'is_superuser')}),
        ('Qo‘shimcha', {'fields': ('avatar', 'bio')}),
        ('Sanalar', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'is_approved'),
        }),
    )

    actions = ['approve_users']

    def approve_users(self, request, queryset):
        count = queryset.update(is_approved=True)
        self.message_user(request, f"{count} ta foydalanuvchi tasdiqlandi.")
    approve_users.short_description = "Tanlanganlarni tasdiqlash"