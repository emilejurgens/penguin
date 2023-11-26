from tasks.models import User
from django.test import TestCase
from tasks.models import Task
from django.utils import timezone
from tasks.forms import TaskForm
from datetime import timedelta
from django.urls import reverse


class TestTaskModel(TestCase):
    fixtures = ['tasks/tests/fixtures/default_user.json']

    def setUp(self):
        self.user = User.objects.get(username='@johndoe')
        self.form_input = {
            'title': 'Test Task',
            'description': 'Test description',
            'due_date': timezone.now().date(),
            'status':'pending',
            'assigned_to':[self.user.id]
        }

    def test_form_is_valid(self):
        form = TaskForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_invalid_due_date(self):
        form_input = {
            'title': 'Test Task',
            'description': 'Test Description',
            'due_date': timezone.localdate() - timedelta(days=1),
            'status': 'pending',
            'assigned_to':[self.user.id]
        }
        form = TaskForm(data=form_input)
        self.assertFalse(form.is_valid())


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')

        