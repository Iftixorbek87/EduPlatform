from django.db import models
from django.contrib.auth import get_user_model
from courses.models import Course

User = get_user_model()

class Payment(models.Model):
    PAYMENT_CHOICES = (
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('payze', 'Payze'),
    )
    STATUS_CHOICES = (
        ('waiting', 'Kutilmoqda'),
        ('paid', 'To‘landi'),
        ('canceled', 'Bekor qilindi'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_system = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='waiting')
    merchant_trans_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} → {self.course} ({self.get_payment_system_display()})"