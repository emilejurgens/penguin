from django.core.management.base import BaseCommand, CommandError

from tasks.models import User, Task, Team

import pytz
from faker import Faker
from random import randint, random, sample, shuffle

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
    TASKS_COUNT = 50

    def __init__(self):
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        self.create_users()
        self.users = User.objects.all()
        self.create_teams()

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

def create_username(first_name, last_name):
    return '@' + first_name.lower() + last_name.lower()

def create_email(first_name, last_name):
    return first_name + '.' + last_name + '@example.org'
