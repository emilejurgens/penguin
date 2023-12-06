"""Tests of the create team view."""
from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse
from tasks.forms import CreateTeamForm
from tasks.models import User, Team
from tasks.tests.helpers import LogInTester

class CreateTeamViewTestCase(TestCase, LogInTester):
    """Tests of the create team view."""

    databases = "__all__"

    fixtures = ['tasks/tests/fixtures/default_user.json', 
                'tasks/tests/fixtures/other_users.json',]

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.janeDoe = User.objects.get(username='@janedoe')
        self.url = reverse('create_team')
        self.members = [self.user.pk, self.janeDoe.pk]
        self.form_input = {
            'name': 'test team',
            'members': self.members,
        }

    def test_create_team_url(self):
        self.assertEqual(self.url,'/create_team/')

    def test_get_create_team(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertFalse(form.is_bound)

    def test_unsuccesful_team_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        self.form_input['name'] = ''
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, CreateTeamForm))
        self.assertTrue(form.is_bound)

    def test_succesful_team_creation(self):
        self.client.login(username=self.user.username, password='Password123')
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        team_created = Team.objects.get(name='test team')
        self.assertEqual(team_created.name, 'test team')
        self.assertEqual(team_created.members.count(), 2)
        self.assertTrue(team_created.members.filter(username='@johndoe').exists())
        self.assertTrue(team_created.members.filter(username='@janedoe').exists())
        self.assertTrue(self._is_logged_in())
