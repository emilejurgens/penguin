"""Forms for the tasks app."""
from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from .models import User, Team

class LogInForm(forms.Form):
    """Form enabling registered users to log in."""

    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password", widget=forms.PasswordInput())

    def get_user(self):
        """Returns authenticated user if possible."""

        user = None
        if self.is_valid():
            username = self.cleaned_data.get('username')
            password = self.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
        return user


class UserForm(forms.ModelForm):
    """Form to update user profiles."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

class NewPasswordMixin(forms.Form):
    """Form mixing for new_password and password_confirmation fields."""

    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(),
        validators=[RegexValidator(
            regex=r'^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).*$',
            message='Password must contain an uppercase character, a lowercase '
                    'character and a number'
            )]
    )
    password_confirmation = forms.CharField(label='Password confirmation', widget=forms.PasswordInput())

    def clean(self):
        """Form mixing for new_password and password_confirmation fields."""

        super().clean()
        new_password = self.cleaned_data.get('new_password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if new_password != password_confirmation:
            self.add_error('password_confirmation', 'Confirmation does not match password.')


class PasswordForm(NewPasswordMixin):
    """Form enabling users to change their password."""

    password = forms.CharField(label='Current password', widget=forms.PasswordInput())

    def __init__(self, user=None, **kwargs):
        """Construct new form instance with a user instance."""
        
        super().__init__(**kwargs)
        self.user = user

    def clean(self):
        """Clean the data and generate messages for any errors."""

        super().clean()
        password = self.cleaned_data.get('password')
        if self.user is not None:
            user = authenticate(username=self.user.username, password=password)
        else:
            user = None
        if user is None:
            self.add_error('password', "Password is invalid")

    def save(self):
        """Save the user's new password."""

        new_password = self.cleaned_data['new_password']
        if self.user is not None:
            self.user.set_password(new_password)
            self.user.save()
        return self.user


class SignUpForm(NewPasswordMixin, forms.ModelForm):
    """Form enabling unregistered users to sign up."""

    class Meta:
        """Form options."""

        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def save(self):
        """Create a new user."""

        super().save(commit=False)
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('new_password'),
        )
        return user
    
class CreateTeamForm(forms.ModelForm):
    pass
    
class EditTeamForm(forms.Form):
    """Form enabling users to add and delete team members and change team's name."""

    old_name = forms.CharField(
        label = 'Current Team Name', 
        required = True, 
        max_length = 30
    )
    new_name = forms.CharField(
        label = 'New Team Name', 
        required = False,
        max_length = 30
    )
    members_to_add = forms.ModelMultipleChoiceField(
        queryset = User.objects.all().order_by('username'), 
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required = False
    )
    members_to_delete = forms.ModelMultipleChoiceField(
        queryset = User.objects.all().order_by('username'),  
        widget = forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        required = False
    )

    def clean(self):
        cleaned_data = super().clean()
        old_name = cleaned_data.get('old_name')
        new_name = cleaned_data.get('new_name')

        try:
            team = Team.objects.get(name=old_name)
        except Team.DoesNotExist:
            self.add_error('old_name', 'Team with this name does not exist')
            raise forms.ValidationError("Team with this name does not exist.")
        
        if new_name:
            try:
                team_with_new_name = Team.objects.get(name=new_name)
                self.add_error('new_name', 'Team with this name already exists')
            except Team.DoesNotExist:
                pass
        

        return cleaned_data
    
    def save(self):
        """Save the changes made to a team."""
        old_team_name = self.cleaned_data['old_name']
        new_name = self.cleaned_data['new_name']
        members_to_add = self.cleaned_data['members_to_add']
        members_to_delete = self.cleaned_data['members_to_delete']
        try:
            team = Team.objects.get(name=old_team_name)
            if new_name:
                team.name = new_name

            if members_to_add:
                team.members.add(*members_to_add)

            if members_to_delete:
                team.members.remove(*members_to_delete)
            team.save()
        except Team.DoesNotExist:
            raise forms.ValidationError("Team with this name does not exist!")