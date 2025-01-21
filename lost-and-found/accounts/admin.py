from django.contrib import admin
from .models import UserProfile, Faculty, Reward
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'user',
        'faculty',
        'avatar'
    ]

class FacultyAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'faculty_name'
    ]

class RewardAdmin(admin.ModelAdmin):
    list_display = ['user', 'points', 'created_at']

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Faculty, FacultyAdmin)
admin.site.register(Reward, RewardAdmin)