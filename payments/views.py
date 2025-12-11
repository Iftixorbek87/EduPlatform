from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from courses.models import Course
from .models import Payment
import hashlib
import json
import base64

@login_required
def create_payment(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.price == 0:
        # Bepul kurs – darhol ochamiz
        from courses.models import Enrollment
        Enrollment.objects.get_or_create(student=request.user, course=course)
        return redirect('course_detail', pk=course_id)

    # Oldin to‘langanmi?
    if Payment.objects.filter(user=request.user, course=course, status='paid').exists():
        return redirect('course_detail', pk=course_id)

    return render(request, 'payments/choose.html', {'course': course})

# CLICK
def click_prepare(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    amount = int(course.price * 100)  # tiyinlarda

    payment = Payment.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        payment_system='click',
        merchant_trans_id=f"course_{course.id}_{request.user.id}"
    )

    click_url = (
        f"https://my.click.uz/services/pay?service_id=12345"  # test ID
        f"&merchant_id=12345"  # test ID
        f"&amount={amount}"
        f"&transaction_param={payment.id}"
        f"&return_url=https://your-site.com/payments/success/{payment.id}/"
    )
    return redirect(click_url)

# PAYME
def payme_prepare(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    amount = int(course.price * 100)

    payment = Payment.objects.create(
        user=request.user,
        course=course,
        amount=course.price,
        payment_system='payme',
        merchant_trans_id=f"course_{course.id}_{request.user.id}"
    )

    payme_data = {
        "method": "CreateTransaction",
        "params": {
            "account": {"payment_id": payment.id},
            "amount": amount,
            "callback": f"https://your-site.com/payments/payme/callback/",
            "return": f"https://your-site.com/payments/success/{payment.id}/"
        }
    }

    token = "your_payme_merchant_key"  # test rejim uchun
    encoded = base64.b64encode(json.dumps(payme_data).encode()).decode()
    return redirect(f"https://checkout.payme.uz/{token}/{encoded}")

# Webhook va muvaffaqiyat sahifasi
@csrf_exempt
def payment_success(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == "POST":
        # Bu yerda real webhook keladi – test uchun shartli qilamiz
        payment.status = 'paid'
        payment.save()

        # Kursni ochamiz
        from courses.models import Enrollment
        Enrollment.objects.get_or_create(student=payment.user, course=payment.course)

    return render(request, 'payments/success.html', {'payment': payment})