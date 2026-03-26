from django.contrib import admin
from .models import Course, Enrollment, CourseMaterial, Progress, Review


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "instructor",
        "price",
        "discount_percent",
        "discount_active",
        "created_at"
    )

    list_filter = (
        "discount_active",
        "created_at"
    )

    search_fields = (
        "title",
        "instructor__username"
    )


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        "student",
        "course",
        "enrolled_at"
    )

    search_fields = (
        "student__username",
        "course__title"
    )


@admin.register(CourseMaterial)
class CourseMaterialAdmin(admin.ModelAdmin):

    list_display = (
        "course",
        "title",
        "material_type",
        "uploaded_at"
    )


admin.site.register(Progress)
admin.site.register(Review)