from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import (
    Course,
    CourseMaterial,
    Enrollment,
    Progress,
    Review
)

# =========================
# INSTRUCTOR: CREATE COURSE
# =========================
@login_required
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image = request.FILES.get('image')

        price = request.POST.get('price')
        discount_percent = request.POST.get('discount_percent') or 0
        discount_active = True if request.POST.get('discount_active') else False

        Course.objects.create(
            instructor=request.user,
            title=title,
            description=description,
            image=image,
            price=price,
            discount_percent=discount_percent,
            discount_active=discount_active
        )

        return redirect('dashboard')

    return render(request, 'courses/create_course.html')


# =========================
# INSTRUCTOR: MY COURSES
# =========================
@login_required
def instructor_courses(request):
    courses = Course.objects.filter(instructor=request.user)

    return render(request, 'courses/instructor_courses.html', {
        'courses': courses
    })


# =========================
# INSTRUCTOR: COURSE STUDENTS
# =========================
@login_required
def course_students(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related("student")

    # Attach review for each student
    for enrollment in enrollments:
        enrollment.review = Review.objects.filter(
            course=course,
            student=enrollment.student
        ).first()

    return render(request, "courses/course_students.html", {
        "course": course,
        "enrollments": enrollments
    })

# =========================
# INSTRUCTOR: DELETE COURSE
# =========================
@login_required
def delete_course(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    if request.method == 'POST':
        course.delete()
        return redirect('instructor_courses')

    return render(request, 'courses/delete_course_confirm.html', {
        'course': course
    })


# =========================
# STUDENT: BROWSE COURSES
# =========================
@login_required
def browse_courses(request):
    query = request.GET.get('q', '')

    if query:
        courses = Course.objects.filter(title__icontains=query)
    else:
        courses = Course.objects.all()

    return render(request, 'courses/browse_courses.html', {
        'courses': courses,
        'query': query
    })


# =========================
# STUDENT: ENROLL COURSE
# =========================
@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment, created = Enrollment.objects.get_or_create(
        student=request.user,
        course=course
    )

    if created:
        Progress.objects.create(enrollment=enrollment)

    return redirect('my_courses')


# =========================
# STUDENT: MY COURSES
# =========================
@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user)

    return render(request, 'courses/my_courses.html', {
        'enrollments': enrollments
    })


# =========================
# STUDENT: PROGRESS
# =========================
@login_required
def progress_view(request):
    progress = Progress.objects.filter(
        enrollment__student=request.user
    )

    return render(request, 'courses/progress.html', {
        'progress': progress
    })


# =========================
# INSTRUCTOR: ADD MATERIAL
# =========================
@login_required
def add_material(request, course_id):
    course = get_object_or_404(
        Course,
        id=course_id,
        instructor=request.user
    )

    if request.method == 'POST':
        CourseMaterial.objects.create(
            course=course,
            title=request.POST.get('title'),
            material_type=request.POST.get('material_type'),
            file=request.FILES.get('file')
        )

        return redirect('instructor_courses')

    return render(request, 'courses/add_material.html', {
        'course': course
    })


# =========================
# STUDENT: COURSE DETAIL
# =========================
@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    enrollment = get_object_or_404(
        Enrollment,
        student=request.user,
        course=course
    )

    materials = course.materials.all()
    reviews = course.reviews.select_related("student")

    student_review = Review.objects.filter(
        course=course,
        student=request.user
    ).first()

    return render(request, 'courses/course_detail.html', {
        'course': course,
        'materials': materials,
        'enrollment': enrollment,
        'reviews': reviews,
        'student_review': student_review,
    })


# =========================
# STUDENT: ADD / EDIT REVIEW
# =========================
@login_required
def add_review(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure student is enrolled
    get_object_or_404(
        Enrollment,
        student=request.user,
        course=course
    )

    review = Review.objects.filter(
        course=course,
        student=request.user
    ).first()

    if request.method == "POST":
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        if not rating or not comment:
            return render(request, "courses/add_review.html", {
                "course": course,
                "review": review,
                "error": "Rating and comment are required."
            })

        if review:
            review.rating = rating
            review.comment = comment
            review.save()
        else:
            Review.objects.create(
                course=course,
                student=request.user,
                rating=rating,
                comment=comment
            )

        return redirect("course_detail", course_id=course.id)

    return render(request, "courses/add_review.html", {
        "course": course,
        "review": review,
    })


# =========================
# INSTRUCTOR: COURSE REVIEWS  ✅ (MISSING EARLIER)
# =========================
@login_required
def instructor_course_reviews(request):
    courses = Course.objects.filter(
        instructor=request.user
    ).prefetch_related("reviews", "reviews__student")

    return render(request, "courses/instructor_course_reviews.html", {
        "courses": courses
    })