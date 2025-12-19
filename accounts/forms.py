from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Foydalanuvchi nomingizni kiriting'
        })
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500',
            'placeholder': 'Parolingizni kiriting'
        })
    )

    error_messages = {
        'invalid_login': "Noto'g'ri foydalanuvchi nomi yoki parol.",
        'inactive': "Bu hisob faol emas.",
    }
