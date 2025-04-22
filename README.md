# Unix-Inspired Task Manager API (Django + DRF)

A lightweight RESTful API built with Django & DRF that mimics Unix-like process operations — create (fork), list (ls), delete (rm), update (exit), and monitor tasks, all while supporting multi-user token authentication.

---

## Requirements
Python 3.7+

Django 4.x

Django REST Framework

## ✅ Features

- Task creation (like `fork`)
- Task listing and filtering (like `ls`, `grep`)
- Task deletion (like `rm`)
- Task status update (like `exit`)
- Auto status transition (`running` → `completed/failed`)
- User-based isolation via Token Auth
- Frontend UI (`index.html`)
- CLI Tool (`client.py`)
- Health check endpoint
- Unit tests included

---

## ⚙️ Setup Instructions

### 1. Clone and set up virtual environment

- git clone git@github.com:diwyanshuprasad19/Unix-Inspired-Task-Manager.git
- cd task_manager
- python -m venv venv
- source venv/bin/activate  
# Windows: 
- venv\Scripts\activate

## Install dependencies

- pip install -r requirements.txt

## Apply migrations and create superuser

- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

- Username:admin@local.com

- Password:12345

## Run the development server

- python manage.py runserver

### 🔐 Authentication (Token-based)

Get your token via:

curl -X POST http://127.0.0.1:8000/api-token-auth/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
Add this token to all subsequent API calls:

Authorization: Token 1a6660f8af01595b7548e04504dead3f9ded40b9

API Endpoints

Action	Method	URL

- Get Auth Token	POST	http://127.0.0.1:8000/api-token-auth/
- Create Task	POST	http://127.0.0.1:8000/api/tasks/
- List Tasks	GET	http://127.0.0.1:8000/api/tasks/
- Filter by Status	GET	http://127.0.0.1:8000/api/tasks/?status=completed
- Get Task by ID	GET	http://127.0.0.1:8000/api/tasks/<id>/
- Delete Task	DELETE	http://127.0.0.1:8000/api/tasks/<id>/
- Update Task Status	PATCH	http://127.0.0.1:8000/api/tasks/<id>/
- Health Check	GET	http://127.0.0.1:8000/api/health/


## Frontend UI (index.html)
Open index.html in any browser

Replace your_token_here with your token in the script section

## CLI Tool (client.py)
Usage examples:

- python client.py fork "Clean temp files"
- python client.py ls
- python client.py show 1
- python client.py done 1
- python client.py rm 1
- Make sure to update the token in client.py

## Run Tests

- python manage.py test tasks

