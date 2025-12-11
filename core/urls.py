from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from accounts.views import register_view, CustomLoginView
from core.views import home
from courses.views import course_detail_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home, name='home'),  # Bosh sahifa
    path('register/', register_view, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

    path('course/<int:pk>/', course_detail_view, name='course_detail'),
    path('payments/', include('payments.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)