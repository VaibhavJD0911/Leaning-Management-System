from django.db import models
from django.db.models import Avg
from accounts.models import User


class Course(models.Model):
    instructor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'roles': 'instructor'},
        related_name="courses"
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='course_images/', blank=True, null=True)

    # 💰 PRICING
    price = models.DecimalField(max_digits=8, decimal_places=2)
    discount_percent = models.PositiveIntegerField(default=0)  # 0–100
    discount_active = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    # ⭐ Ratings
    def average_rating(self):
        avg = self.reviews.aggregate(avg=Avg("rating"))["avg"]
        return round(avg, 1) if avg else 0

    def total_reviews(self):
        return self.reviews.count()

    # 💸 Final price logic
    def final_price(self):
        if self.discount_active and self.discount_percent > 0:
            discount_amount = (self.discount_percent / 100) * float(self.price)
            return round(float(self.price) - discount_amount, 2)
        return self.price

    def __str__(self):
        return self.title

class Enrollment(models.Model):
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'roles': 'student'},
        related_name="enrollments"
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments"
    )

    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")  # 🔥 no double enrollment

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"


class Progress(models.Model):
    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name="progress"
    )

    percentage = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.percentage}%"


class CourseMaterial(models.Model):
    MATERIAL_TYPE = (
        ('video', 'Video'),
        ('pdf', 'PDF'),
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='materials'
    )

    title = models.CharField(max_length=200)
    material_type = models.CharField(max_length=10, choices=MATERIAL_TYPE)
    file = models.FileField(upload_to='course_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"


# ⭐ NEW MODEL (IMPORTANT)
class Review(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="reviews"
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'roles': 'student'},
        related_name="reviews"
    )

    rating = models.IntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )

    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("course", "student")  # 🔒 1 review per student

    def __str__(self):
        return f"{self.course.title} - {self.rating}⭐"