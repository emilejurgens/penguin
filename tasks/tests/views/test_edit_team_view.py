"""Tests for the edit team view."""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse
from tasks.forms import EditTeamForm
from tasks.models import User, Team
from tasks.tests.helpers import reverse_with_next

class ProfileViewTest(TestCase):
    """Test of the edit team view."""

    databases = "__all__"

    fixtures = [
        'tasks/tests/fixtures/default_user.json',
        'tasks/tests/fixtures/other_users.json'
    ]

    def setUp(self):
        self.user1 = User.objects.get(username='@johndoe')
        self.team = Team.objects.create(name='Test Team')
        self.url = reverse('edit_team')
        self.form_input = {
            'old_name': 'Test Team',
            'new_name': 'New Team Name',
            'members_to_add': [],
            'members_to_delete': [],
        }

    def test_edit_team_url(self):
        self.assertEqual(self.url, '/edit_team/')

    def test_get_team(self):
        self.client.login(username=self.user1.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTeamForm))

    def test_get_team_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_unsuccesful_team_update(self):
        self.client.login(username=self.user1.username, password='Password123')
        self.form_input['old_name'] = 'Non-existent Name'
        before_count = Team.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_team.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, EditTeamForm))
        self.assertTrue(form.is_bound)

    def test_succesful_team_update(self):
        self.client.login(username=self.user1.username, password='Password123')
        response = self.client.post(self.url, self.form_input, follow=True)
        response_url = reverse('dashboard')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'dashboard.html')
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.SUCCESS)
        updated_team = Team.objects.get(name='New Team Name')
        self.assertEqual(updated_team.name, 'New Team Name')
        self.assertEqual(updated_team.members.count(), 0)
        
      
