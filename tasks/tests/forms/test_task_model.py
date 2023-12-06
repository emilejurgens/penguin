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
            'status':'in_progress',
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
            'status': 'in_progress',
            'assigned_to':[self.user.id]
        }
        form = TaskForm(data=form_input)
        self.assertFalse(form.is_valid())


    def test_view_url_exists_at_desired_location(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)


    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_task.html')

    def test_deleting_a_task(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
        title='Delete Task',
        description='Task to be deleted',
        due_date=timezone.now().date(),
        status='pending',
        created_by=self.user
    )

        response = self.client.post(reverse('delete_task', kwargs={'task_id': task.id}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_updating_a_task(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
        title='Update Task',
        description='update status',
        due_date=timezone.now().date(),
        status='pending',
        created_by=self.user
    )

        new_status = 'completed'
        response = self.client.post(reverse('update_status', kwargs={'task_id': task.id}), {'status': new_status})
        updated_task = Task.objects.get(id=task.id)
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(updated_task.status, new_status)

    def test_changing_a_task(self):
        self.client.force_login(self.user)
        task = Task.objects.create(
            title='Change Task',
            description='changed',
            due_date=timezone.now().date(),
            status='pending',
            created_by=self.user
        )

        response = self.client.get(reverse('create_task', kwargs={'task_id': task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, task.title) 
        self.assertContains(response, task.description)

        