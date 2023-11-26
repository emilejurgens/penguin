"""Unit tests for the Team model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from tasks.models import User
from tasks.models import Team
from tasks.models import Task
 

class UserModelTestCase(TestCase):
    """Unit tests for the User model."""

    
    def setUp(self):
        self.user1 = User.objects.create(username='user1', email = '123@gmail.com')
        self.user2 = User.objects.create(username='user2',  email = '345@gmail.com')
    
        # self.task1 = Task.objects.create(name='Task 1')
        # self.task2 = Task.objects.create(name='Task 2')

    def test_add_members(self):
        team = Team.objects.create(name='Team1')
        team.members.add(self.user1, self.user2)
        self.assertEqual(team.members.count(), 2)
        self.assertIn(self.user1, team.members.all())

    # def test_add_tasks(self):
    #     team = Team.objects.create(name='Team1')
    #     team.tasks.add(self.task1, self.task2)
    #     self.assertEqual(team.tasks.count(), 2)
    #     self.assertIn(self.task2, team.tasks.all())
    

    def test_team_creation(self):
        # Create a team
        team = Team.objects.create(name='Team1')

        # Add members to the team
        team.members.add(self.user1, self.user2)

        # Add tasks to the team
        # team.tasks.add(self.task1, self.task2)

        # Check if members and tasks are associated with the team correctly
        self.assertEqual(team.members.count(), 2)
        # self.assertEqual(team.tasks.count(), 2)

        # Check if specific members and tasks are associated with the team
        self.assertIn(self.user1, team.members.all())
        # self.assertIn(self.task2, team.tasks.all())




 