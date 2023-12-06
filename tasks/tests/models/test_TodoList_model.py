from django.test import TestCase
from tasks.models import TodoItem

class TodoItemModelTest(TestCase):
    def test_string_representation(self):
        todo_item = TodoItem(content='A simple test task')
        self.assertEqual(str(todo_item), 'A simple test task')