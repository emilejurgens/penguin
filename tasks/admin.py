from django.contrib import admin
from .models import User, Team

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Team)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'name'
    ]
# Register your models here.
