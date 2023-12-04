"""Tests of the team view."""
from django.test import TestCase
from django.urls import reverse
from tasks.models import User
from tasks.tests.helpers import reverse_with_next


class TeamViewTestCase(TestCase):
    """Tests of the team view."""

    fixtures = ['tasks/tests/fixtures/default_user.json',
                'tasks/tests/fixtures/other_users.json',
                'tasks/tests/fixtures/default_team.json',]

    def setUp(self):
        self.url = reverse('teams')
        self.user = User.objects.get(username='@johndoe')

    def test_teams_url(self):
        self.assertEqual(self.url,'/teams/')

    def test_get_teams(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'team.html')

    def test_get_teams_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)