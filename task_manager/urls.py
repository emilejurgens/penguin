"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks import views
from tasks.views import create_task, show_all_tasks, delete_task, update_status

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('log_in/', views.LogInView.as_view(), name='log_in'),
    path('log_out/', views.log_out, name='log_out'),
    path('password/', views.PasswordView.as_view(), name='password'),
    path('profile/', views.ProfileUpdateView.as_view(), name='profile'),
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('project/', views.project, name='project'),
    path('all_tasks/', views.all_tasks, name='all_tasks'),
    path('todo/', views.todo, name='todo'),
    path('add_task/', views.add_task, name='add_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('teams/', views.TeamView.as_view(), name='teams'),
    path('create_team/', views.CreateTeamView.as_view(), name='create_team'),
    path('add_members/', views.AddMembersView.as_view(), name='add_members'),
    path('task/create/', create_task, name='create_task'),
    path('task/create/<int:task_id>/', create_task, name='create_task'),
    path('tasks/all/', show_all_tasks, name ='all_tasks'),
    path('task/delete/<int:task_id>/', delete_task, name='delete_task'),
    path('task/update/<int:task_id>/', update_status, name='update_status'),
]


