"""Unit tests for the Team model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User
from tasks.models import Team
from tasks.models import Task
from datetime import date
 

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    databases = "__all__"

    
    def setUp(self):
        self.team = Team.objects.create(name='Test Team')
        self.user1 = User.objects.create(username='@janedoe', email = 'janedoe@example.org')
        self.user2 = User.objects.create(username='@johndoe',  email = 'johndoe@example.org')
    
        self.task1 = Task.objects.create(title='Task 1', due_date = date(2023,3,12), created_by = self.user1)
        self.task2 = Task.objects.create(title='Task 2', due_date = date(2023,4,23), created_by = self.user1)

    def test_valid_team(self):
        self._assert_team_is_valid()

    def test_add_members(self):
        self.team.members.add(self.user1, self.user2)
        self.assertEqual(self.team.members.count(), 2)
        self.assertIn(self.user1, self.team.members.all())

    def test_add_tasks(self):
        self.team.tasks.add(self.task1, self.task2)
        self.assertEqual(self.team.tasks.count(), 2)
        self.assertIn(self.task2, self.team.tasks.all())

    def test_team_name_can_be_30_characters_long(self):
        self.team.name = 'x' * 30
        self._assert_team_is_valid()

    def test_team_name_cannot_be_longer_than_30_characters(self):
        self.team.name = 'x' * 31
        self._assert_team_is_invalid()

    def test_team_name_must_be_unique(self):
        second_team = Team.objects.create(name='Test Team2')
        self.team.name = second_team.name
        self._assert_team_is_invalid()

    def test_team_name_cannot_be_blank(self):
        self.team.name = ''
        self._assert_team_is_invalid()

    def _assert_team_is_valid(self):
        try:
            self.team.full_clean()
        except (ValidationError):
            self.fail('Test team should be valid')

    def _assert_team_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.team.full_clean()