from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:course_id>/', views.create_payment, name='create_payment'),
    path('click/<int:course_id>/', views.click_prepare, name='click_prepare'),
    path('payme/<int:course_id>/', views.payme_prepare, name='payme_prepare'),
    path('success/<int:payment_id>/', views.payment_success, name='payment_success'),
]