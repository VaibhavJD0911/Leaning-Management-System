from django.urls import path
from .views import (
    create_course,
    browse_courses,
    enroll_course,
    my_courses,
    progress_view,
    instructor_courses,
    course_students,
    add_material,
    delete_course,
    course_detail,
    add_review,
    instructor_course_reviews,
)

urlpatterns = [

    # =========================
    # INSTRUCTOR ROUTES
    # =========================
    path('create/', create_course, name='create_course'),
    path('instructor/courses/', instructor_courses, name='instructor_courses'),
    path('instructor/course/<int:course_id>/students/', course_students, name='course_students'),
    path('instructor/course/<int:course_id>/add-material/', add_material, name='add_material'),
    path('instructor/course/<int:course_id>/delete/', delete_course, name='delete_course'),
    path('instructor/reviews/', instructor_course_reviews, name='instructor_course_reviews'),

    # =========================
    # STUDENT ROUTES
    # =========================
    path('browse/', browse_courses, name='browse_courses'),
    path('my-courses/', my_courses, name='my_courses'),
    path('progress/', progress_view, name='progress'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),

    # 📘 Course Detail
    path('course/<int:course_id>/', course_detail, name='course_detail'),

    # ✍️ Student Review
    path('course/<int:course_id>/review/', add_review, name='add_review'),
]
