from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Ro'yxatdan o'tish
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role', 'student')

        if not username or not password1:
            messages.error(request, "Barcha maydonlarni to'ldiring!")
        elif password1 != password2:
            messages.error(request, "Parollar mos emas!")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Bu username allaqachon band!")
        else:
            user = User.objects.create_user(
                username=username,
                password=password1,
                role=role,
                is_approved=False  # Admin tasdiqlamaguncha kirish taqiqlanadi
            )
            messages.success(request, "Muvaffaqiyatli ro'yxatdan o'tdingiz!")
            return redirect('home')

    return render(request, 'auth/register.html')


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        
        # Debug info
        print(f"Login attempt - Username: {username}")
        
        # Try to authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            print(f"User {user} logged in successfully")
            return redirect('home')
        else:
            print("Authentication failed")
            messages.error(request, "Foydalanuvchi nomi yoki parol noto'g'ri")
    
    # If GET request or authentication failed, show login form
    if request.user.is_authenticated:
        return redirect('home')
        
    return render(request, 'auth/login.html')