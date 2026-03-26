import razorpay

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from courses.models import Course, Enrollment, Progress
from .models import Payment


# Razorpay Client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# =========================
# CREATE PAYMENT ORDER
# =========================
@login_required
def create_payment(request, course_id):

    course = get_object_or_404(Course, id=course_id)

    amount = int(course.final_price() * 100)  # Razorpay uses paisa

    order_data = {
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    }

    order = client.order.create(data=order_data)

    payment = Payment.objects.create(
        student=request.user,
        course=course,
        amount=course.final_price(),
        razorpay_order_id=order["id"]
    )

    context = {
        "course": course,
        "payment": payment,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
        "amount": amount,
        "order_id": order["id"],
    }

    return render(request, "payments/checkout.html", context)


# =========================
# VERIFY PAYMENT
# =========================
@csrf_exempt
def verify_payment(request):

    if request.method == "POST":

        payment_id = request.POST.get("razorpay_payment_id")
        order_id = request.POST.get("razorpay_order_id")
        signature = request.POST.get("razorpay_signature")

        payment = get_object_or_404(Payment, razorpay_order_id=order_id)

        data = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature
        }

        try:
            client.utility.verify_payment_signature(data)

            payment.razorpay_payment_id = payment_id
            payment.razorpay_signature = signature
            payment.status = "success"
            payment.save()

            # Create enrollment after successful payment
            enrollment, created = Enrollment.objects.get_or_create(
                student=payment.student,
                course=payment.course
            )

            if created:
                Progress.objects.create(enrollment=enrollment)

            return redirect("payment_success")

        except:
            payment.status = "failed"
            payment.save()

            return redirect("payment_failed")


# =========================
# PAYMENT SUCCESS PAGE
# =========================
@login_required
def payment_success(request):
    return render(request, "payments/payment_success.html")


# =========================
# PAYMENT FAILED PAGE
# =========================
@login_required
def payment_failed(request):
    return render(request, "payments/payment_failed.html")