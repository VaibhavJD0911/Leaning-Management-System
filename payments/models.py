from django.db import models

from accounts.models import User
from courses.models import Course

class Payment(models.Model):

    student =models.ForeignKey(User, on_delete=models.CASCADE)

    course=models.ForeignKey(Course, on_delete=models.CASCADE)

    amount=models.DecimalField(max_digits=8 ,decimal_places=2)
    
    razorpay_order_id = models.CharField(max_length=255)

    razorpay_payment_id = models.CharField(max_length=255 ,blank=True ,null=True)
    
    razorpay_signature = models.CharField(max_length=255,blank=True ,null=True)

    status =models.CharField(max_length=20,default="pending")

    created_at =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.course}"

