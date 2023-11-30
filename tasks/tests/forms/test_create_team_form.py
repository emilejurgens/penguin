"""Unit tests of the create team form."""
from django.test import TestCase
from tasks.forms import CreateTeamForm
from tasks.models import User, Team

class CreateTeamFormTest(TestCase):
    """Unit tests of the create team form."""
    def setUp(self):
            User.objects.create_user(username='@user1', password='Password123', email = 'testuser1@example.org')
            User.objects.create_user(username='@user2', password='Password123', email = 'testuser2@example.org')
            self.form_input = {
                'name': 'Test Team',
                'members': User.objects.filter(username__in=['@user1', '@user2']).values_list('id', flat=True), 
            }

    def test_valid_sign_up_form(self):
        form = CreateTeamForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = CreateTeamForm()
        self.assertIn('name', form.fields)

    def test_form_uses_model_validation(self):
        self.form_input['name'] = 'badnamebadnamebadnamebadnamebadname'
        form = CreateTeamForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_form_must_save_correctly(self):
        form = CreateTeamForm(data=self.form_input)
        before_count = Team.objects.count()
        form.save()
        after_count = Team.objects.count()
        self.assertEqual(after_count, before_count+1)
        team = Team.objects.get(name='Test Team')
        self.assertEqual(team.name, 'Test Team')
        member_usernames = ", ".join([user.username for user in team.members.all()])
        expected_members = '@user1, @user2'
        self.assertEqual(member_usernames, expected_members)