from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Task, Team

import pytz
from faker import Faker
from random import randint, random, sample, shuffle
from datetime import datetime, timedelta

user_fixtures = [
    {'username': '@johndoe', 'email': 'john.doe@example.org', 'first_name': 'John', 'last_name': 'Doe'},
    {'username': '@janedoe', 'email': 'jane.doe@example.org', 'first_name': 'Jane', 'last_name': 'Doe'},
    {'username': '@charlie', 'email': 'charlie.johnson@example.org', 'first_name': 'Charlie', 'last_name': 'Johnson'},
]

class Command(BaseCommand):
    """Build automation command to seed the database."""

    USER_COUNT = 300
    DEFAULT_PASSWORD = 'Password123'
    help = 'Seeds the database with sample data'
    TEAM_COUNT = 30
    TASK_COUNT = 50

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.create_teams()
        self.create_tasks()

    def create_users(self):
        self.generate_user_fixtures()
        self.generate_random_users()

    def generate_user_fixtures(self):
        for data in user_fixtures:
            self.try_create_user(data)

    def generate_random_users(self):
        user_count = User.objects.count()
        while  user_count < self.USER_COUNT:
            print(f"Seeding user {user_count}/{self.USER_COUNT}", end='\r')
            self.generate_user()
            user_count = User.objects.count()
        print("User seeding complete.      ")

    def generate_user(self):
        first_name = self.faker.first_name()
        last_name = self.faker.last_name()
        email = create_email(first_name, last_name)
        username = create_username(first_name, last_name)
        self.try_create_user({'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
       
    def try_create_user(self, data):
        try:
            self.create_user(data)
        except:
            pass

    def create_user(self, data):
        User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=Command.DEFAULT_PASSWORD,
            first_name=data['first_name'],
            last_name=data['last_name'],
        )
    
    def create_teams(self):
        self.generate_team_fixtures()
        self.generate_random_teams()

    def generate_team_fixtures(self):
        team_name = "penguin"
        member1 = User.objects.get(username='@johndoe')
        member2 = User.objects.get(username='@janedoe')
        member3 = User.objects.get(username='@charlie')
        new_team = Team.objects.create(name=team_name)
        new_team.members.add(member1)
        new_team.members.add(member2)
        new_team.members.add(member3)

    def generate_random_teams(self):
        team_count = Team.objects.count()
        while team_count < self.TEAM_COUNT:
            print(f"Seeding team {team_count}/{self.TEAM_COUNT}", end='\r')
            self.generate_team()
            team_count = Team.objects.count()
        print("Team seeding complete.      ")

    def generate_team(self):
        team_name = self.faker.word()
        existing_users = list(User.objects.all())
        subset_size = randint(2, 10)
        shuffle(existing_users)
        members_to_add = existing_users[:subset_size]
        self.try_create_team({'name': team_name, 'members': members_to_add})

    def try_create_team(self, data):
        try:
            self.create_team(data)
        except:
            pass

    def create_team(self, data):
        team_name = data['name']
        new_team = Team.objects.create(name=team_name)
        for member_username in data['members']:
            member = User.objects.get(username=member_username)
            new_team.members.add(member)

    def create_tasks(self):
        self.generate_random_tasks()

    def generate_random_tasks(self):
        task_count = Task.objects.count()
        while  task_count < self.TASK_COUNT:
            print(f"Seeding task {task_count}/{self.TASK_COUNT}", end='\r')
            self.generate_task()
            task_count = Task.objects.count()
        print("Task seeding complete.      ")

    def generate_random_date(self):
        start_date = datetime.strptime('2025-01-01', '%Y-%m-%d')
        end_date = datetime.strptime('2026-01-01', '%Y-%m-%d')

        random_date = start_date + timedelta(days=randint(0, (end_date - start_date).days))
        return random_date.strftime('%Y-%m-%d')
    
    def generate_task(self):
        title = self.faker.word()
        description = self.faker.sentence()
        due_date = self.generate_random_date()
        status = self.faker.random_element(elements=['in_progress', 'completed'])
        created_by = User.objects.order_by('?').first()
        assigned_to = User.objects.order_by('?').first()
        self.try_create_task({'title': title, 'description': description, 'due_date': due_date, 'status': status, 'created_by': created_by, 'assigned_to': assigned_to})

    def try_create_task(self, data):
        try:
            self.create_task(data)
        except:
            pass

    def create_task(self, data):
        assigned_user_id = data['assigned_to'].id
        task = Task.objects.create(
            title=data['title'],
            description=data['description'],
            due_date=data['due_date'],
            status=data['status'],
            created_by=data['created_by'],
        )
        task.assigned_to.set([assigned_user_id])

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'
