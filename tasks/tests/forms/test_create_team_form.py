"""Unit tests of the create team form."""
from django.contrib.auth.hashers import check_password
from django import forms
from django.test import TestCase
from tasks.forms import CreateTeamForm
from tasks.models import User, Team

class CreateTeamFormTestCase(TestCase):
    """Unit tests of the create team form."""

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.members = [User.objects.get(username='@johndoe'), User.objects.get(username='@janedoe')]
        self.form_input = {
            'name': 'test team',
            'members': self.members,
        }

    def test_valid_sign_up_form(self):
        form = CreateTeamForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateTeamForm()
        self.assertIn('name', form.fields)
        self.assertIn('members', form.fields)
        members_field = form.fields['members']
        self.assertTrue(isinstance(members_field, forms.ModelMultipleChoiceField))
        members_widget = form.fields['members'].widget
        self.assertTrue(isinstance(members_widget, forms.CheckboxSelectMultiple))

    def test_team_must_have_name(self):
        self.form_input['name'] = ''
        form = CreateTeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_team_must_have_members(self):
        self.form_input['members'] = ''
        form = CreateTeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = CreateTeamForm(data=self.form_input)
        before_count = Team.objects.count()
        form.save()
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        current_team = Team.objects.get(name='test team')
        self.assertEqual(current_team.name, 'test team')
        self.assertEqual(current_team.members.count(), 2)
        self.assertTrue(current_team.members.filter(username='@johndoe').exists())
        self.assertTrue(current_team.members.filter(username='@janedoe').exists())