# Team Penguin Small Group project

## Team members
The members of the team are:
- Emile Jurgens
- Sara Alaqeel
- Adil Mazhitov
- Zoya Nasir
- Kamila Shadieva

## Project structure
The project is called `task_manager`.  It currently consists of a single app `tasks`.

## Deployed version of the application
The deployed version of the application can be found at [*http://adilmazhitov.pythonanywhere.com/*](*enter_url_here*).

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the databases:

```
$ python3 manage.py migrate
$ python3 manage.py migrate --database=logs
```

Seed the development database with:

```
$ python3 manage.py seed
```

Run all tests with:
```
$ python3 manage.py test
```

*The above instructions should work in your version of the application.  If there are deviations, declare those here in bold.  Otherwise, remove this line.*

## Sources
The packages used by this application are specified in `requirements.txt`

The source code: https://github.com/sebatyler/django-user-activity-log
Number of lines of code reused: 13
These code reused in: settings.py (12 line), models.py (1 line)