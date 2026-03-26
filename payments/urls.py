from django.urls import path
from .views import (
    create_payment,
    verify_payment,
    payment_success,
    payment_failed
)

urlpatterns = [

    # Create Razorpay Order
    path('buy/<int:course_id>/', create_payment, name='create_payment'),

    # Razorpay Verification
    path('verify/', verify_payment, name='verify_payment'),

    # Payment result pages
    path('success/', payment_success, name='payment_success'),
    path('failed/', payment_failed, name='payment_failed'),
]