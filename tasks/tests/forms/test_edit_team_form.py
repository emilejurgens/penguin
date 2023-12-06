"""Unit tests of the add team members form."""
from django.test import TestCase
from tasks.forms import EditTeamForm
from tasks.models import Team, User

class EditTeamFormTest(TestCase):
    """Unit tests of the add team members form."""
    def setUp(self):
        self.user1 = User.objects.create(username='@janedoe', email='janedoe@example.org')
        self.user2 = User.objects.create(username='@johndoe', email='johndoe@example.org')
        self.team = Team.objects.create(name='Test Team')

    def test_form_can_just_add_members(self):
        form_input = {
            'old_name': 'Test Team',
            'new_name': None,
            'members_to_add': [self.user1, self.user2],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())

    def test_form_can_just_delete_members(self):
        form_input = {
            'old_name': 'Test Team',
            'new_name': None,
            'members_to_add': [],
            'members_to_delete': [self.user1, self.user2],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())

    def test_form_can_just_change_team_name(self):
        form_input = {
            'old_name': 'Test Team',
            'new_name': 'New Team Name',
            'members_to_add': [],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())

    def test_edit_team_with_invalid_current_team_name(self):
        form_input = {
            'old_name': 'Non-existent Team', 
            'new_name': 'New Team Name',
            'members_to_add': [self.user1, self.user2],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_contain_current_team_name(self):
        form_input = {
            'old_name': None,
            'members': [self.user1],
        }
        form = EditTeamForm(data = form_input)
        self.assertFalse(form.is_valid())

    def test_form_with_invalid_new_team_name(self):
        form_input = {
            'old_name': 'Non-existent Team', 
            'new_name': 'test' * 8,
            'members_to_add': [self.user1, self.user2],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertFalse(form.is_valid())

    def test_form_with_new_team_name_that_already_exists(self):
        team = Team.objects.create(name='Test Team1')
        form_input = {
            'old_name': 'Test Team', 
            'new_name': 'Test Team1',
            'members_to_add': [self.user1, self.user2],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertFalse(form.is_valid())
        
    def test_form_must_save_correctly_when_deleting_members(self):
        self.team.members.add(self.user1, self.user2)
        form_input = {
            'old_name': 'Test Team',
            'new_name': 'New Team Name',
            'members_to_add': [],
            'members_to_delete': [self.user1, self.user2],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())
        form.save()  

        updated_team = Team.objects.get(name='New Team Name')
        self.assertEqual(updated_team.members.count(), 0)

    def test_form_must_save_correctly_when_adding_members(self):
        form_input = {
            'old_name': 'Test Team',
            'new_name': 'New Team Name',
            'members_to_add': [self.user1, self.user2],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())
        form.save()  

        updated_team = Team.objects.get(name='New Team Name')
        self.assertEqual(updated_team.members.count(), 2)

    def test_form_must_save_correctly_when_changing_name(self):
        form_input = {
            'old_name': 'Test Team',
            'new_name': 'New Team Name',
            'members_to_add': [],
            'members_to_delete': [],
        }
        form = EditTeamForm(data=form_input)
        self.assertTrue(form.is_valid())
        form.save()  

        updated_team = Team.objects.get(name='New Team Name')
        self.assertEqual(updated_team.members.count(), 0)