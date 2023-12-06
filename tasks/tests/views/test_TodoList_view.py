# tests/views/test_views.py

from django.test import TestCase
from django.urls import reverse
from tasks.models import TodoItem

class TodoListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/todos/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todo_list.html')
