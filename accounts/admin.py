from django.contrib import admin
from .models import User

# Register your models here.

admin.site.register(User)

admin.site.site_header = "LMS Administration"
admin.site.site_title = "LMS Admin"
admin.site.index_title = "Welcome to LMS Dashboard"
