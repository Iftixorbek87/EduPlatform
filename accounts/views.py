from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from .models import User


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
            messages.success(request, "Ro'yxatdan o'tdingiz! Admin tasdiqlashini kuting.")
            return redirect('login')

    return render(request, 'auth/register.html')


# Login – faqat tasdiqlangan foydalanuvchilar kiradi
class CustomLoginView(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.get_user()
        if not user.is_approved and not user.is_superuser:
            messages.error(self.request, "Hisobingiz hali tasdiqlanmagan. Admin bilan bog'laning.")
            return redirect('login')
        messages.success(self.request, f"Xush kelibsiz, {user.username}!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')