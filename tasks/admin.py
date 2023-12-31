from django.contrib import admin
from .models import User, Team, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for users."""

    list_display = [
        'username', 'first_name', 'last_name', 'email', 'is_active',
    ]

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for teams."""

    list_display = [
        'name',
    ]

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configuration of the admin interface for tasks."""
    list_display = [
        'title', 'user', 'description', 'due_date', 'status', 'created_by',
    ]