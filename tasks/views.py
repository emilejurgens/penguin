from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic.edit import FormView, UpdateView
from django.urls import reverse
from tasks.forms import LogInForm, PasswordForm, UserForm, SignUpForm, TaskForm, CreateTeamForm, AddMembersForm
from tasks.helpers import login_prohibited
from .models import TodoItem, Task 
from django.http import HttpResponseRedirect
from .models import User, Team
from django.views.generic import ListView


@login_required

def dashboard(request):

    if not request.session.get('welcome_message_displayed', False):
        request.session['welcome_message_displayed'] = True
        context = {'show_welcome_message': True}
    else:
        context = {'show_welcome_message': False}

    return render(request, 'dashboard.html', context)


@login_prohibited
def home(request):
    """Display the application's start/home screen."""

    return render(request, 'home.html') 

def create_team(request):
    return render(request, 'create_team.html')

def team(request):
    return render(request, 'team.html')

def project(request):
    return render(request, 'project.html')

def all_tasks(request):
    return render(request, 'all_tasks.html')

def todo(request):
    return render(request, 'todo.html')




class LoginProhibitedMixin:
    """Mixin that redirects when a user is logged in."""

    redirect_when_logged_in_url = None

    def dispatch(self, *args, **kwargs):
        """Redirect when logged in, or dispatch as normal otherwise."""
        if self.request.user.is_authenticated:
            return self.handle_already_logged_in(*args, **kwargs)
        return super().dispatch(*args, **kwargs)

    def handle_already_logged_in(self, *args, **kwargs):
        url = self.get_redirect_when_logged_in_url()
        return redirect(url)

    def get_redirect_when_logged_in_url(self):
        """Returns the url to redirect to when not logged in."""
        if self.redirect_when_logged_in_url is None:
            raise ImproperlyConfigured(
                "LoginProhibitedMixin requires either a value for "
                "'redirect_when_logged_in_url', or an implementation for "
                "'get_redirect_when_logged_in_url()'."
            )
        else:
            return self.redirect_when_logged_in_url


class LogInView(LoginProhibitedMixin, View):
    """Display login screen and handle user login."""

    http_method_names = ['get', 'post']
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def get(self, request):
        """Display log in template."""

        self.next = request.GET.get('next') or ''
        return self.render()

    def post(self, request):
        """Handle log in attempt."""
        form = LogInForm(request.POST)
        self.next = request.POST.get('next') or settings.REDIRECT_URL_WHEN_LOGGED_IN
        user = form.get_user()
        if user is not None:
            login(request, user)
            return redirect(self.next)
        messages.add_message(request, messages.ERROR, "The credentials provided were invalid!")
        return self.render()

    def render(self):
        """Render log in template with blank log in form."""

        form = LogInForm()
        return render(self.request, 'log_in.html', {'form': form, 'next': self.next})


def log_out(request):
    """Log out the current user"""

    logout(request)
    return redirect('home')


class PasswordView(LoginRequiredMixin, FormView):
    """Display password change screen and handle password change requests."""

    template_name = 'password.html'
    form_class = PasswordForm

    def get_form_kwargs(self, **kwargs):
        """Pass the current user to the password change form."""

        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        """Handle valid form by saving the new password."""

        form.save()
        login(self.request, self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect the user after successful password change."""

        messages.add_message(self.request, messages.SUCCESS, "Password updated!")
        return reverse('dashboard')


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Display user profile editing screen, and handle profile modifications."""

    model = UserForm
    template_name = "profile.html"
    form_class = UserForm

    def get_object(self):
        """Return the object (user) to be updated."""
        user = self.request.user
        return user

    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Profile updated!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)


class SignUpView(LoginProhibitedMixin, FormView):
    """Display the sign up screen and handle sign ups."""

    form_class = SignUpForm
    template_name = "sign_up.html"
    redirect_when_logged_in_url = settings.REDIRECT_URL_WHEN_LOGGED_IN

    def form_valid(self, form):
        self.object = form.save()
        login(self.request, self.object)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
    

#To do list       
def todo(request):
    tasks = TodoItem.objects.all()
    return render(request, 'todo.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        new_task = TodoItem(content=request.POST['content'])
        new_task.save()
    return redirect('todo')  

def delete_task(request, task_id):
    task_to_delete = TodoItem.objects.get(id=task_id)
    task_to_delete.delete()
    return redirect('todo')


    
class TeamView(LoginRequiredMixin, ListView):
    """Display the team screen."""
    model = Team
    template_name = "team.html"
    context_object_name = 'teams'

    def get_queryset(self):
        current_user = self.request.user
        teams = Team.objects.filter(members=current_user)
        return teams

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
    
    
class CreateTeamView(LoginRequiredMixin, FormView):
    """Display the create team screen."""

    model = CreateTeamForm
    form_class = CreateTeamForm
    template_name = "create_team.html"
    

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Team created!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
class AddMembersView(LoginRequiredMixin, View):
    """Display the add members screen."""
    
    model = AddMembersForm
    form_class = AddMembersForm
    template_name = "add_members.html"

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        """Return redirect URL after successful update."""
        messages.add_message(self.request, messages.SUCCESS, "Team member added!")
        return reverse(settings.REDIRECT_URL_WHEN_LOGGED_IN)
    
    def get(self, request):
        return render(request, 'add_members.html')

def create_task(request, task_id = None):
    if task_id:
        task = get_object_or_404(Task,pk=task_id, created_by=request.user)
        form = TaskForm(request.POST or None, instance = task)
    else:
        form = TaskForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.user = request.user
            task.save()
            form.save_m2m()
            return redirect ('all_tasks')

    return render(request, 'create_task.html', {'form':form})

def show_all_tasks(request):
    all_tasks = Task.objects.all()
    for task in all_tasks:
        print(task.title, task.assigned_to.all())
    return render(request, 'all_tasks.html', {'all_tasks': all_tasks})

def update_status(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.status = request.POST.get('status')
        task.save()
        return redirect('all_tasks')
    return render(request, 'update_task.html', {'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if task.created_by == request.user: 
        task.delete()
    return redirect('all_tasks')