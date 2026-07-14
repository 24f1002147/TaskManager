# TaskManager


# Task Manager App

A simple full stack task manager app built with Flask and VueJS. Made as part of App Dev placement preparation activity (Activity 1).

## Overview

This is a basic task management web app where users can register, log in, and manage their own personal to-do list. Built to demonstrate REST API development, token based authentication, and CRUD operations using the Flask + VueJS stack.

## Features

- User registration and login
- Token based authentication (Flask-Security)
- Create, read, update, delete tasks
- Mark tasks as done / not done
- Set task priority (low / medium / high)
- Each user can only see and manage their own tasks

## Tech Stack

**Backend:** Flask, Flask-SQLAlchemy, Flask-Security-Too, Flask-Cors, SQLite
**Frontend:** VueJS 3 (via CDN, no build step), Axios

## Project Structure

```
task-manager/
├── backend/
│   ├── app.py
│   └── requirements.txt
├── frontend/
│   └── index.html
└── README.md
```

## Installation

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The server will start on `http://127.0.0.1:5000`

### Frontend

Open `frontend/index.html` directly in your browser.

If you run into CORS issues opening the file directly, serve it instead:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## API Documentation

### `POST /api/register`
Registers a new user.

**Body:**
```json
{ "email": "user@example.com", "password": "yourpassword" }
```

### `POST /api/login`
Logs in and returns an auth token.

**Body:**
```json
{ "email": "user@example.com", "password": "yourpassword" }
```

**Response:**
```json
{ "token": "...", "email": "user@example.com", "user_id": 1 }
```

> All routes below require the header: `Authentication-Token: <token>`

### `GET /api/tasks`
Returns all tasks belonging to the logged in user.

### `POST /api/tasks`
Creates a new task.

**Body:**
```json
{ "title": "Buy groceries", "desc": "milk, eggs, bread", "priority": "high" }
```

### `PUT /api/tasks/<id>`
Updates a task. Send any of `title`, `desc`, `done`, `priority` in the body.

### `DELETE /api/tasks/<id>`
Deletes a task.

## Notes

- The SQLite database (`taskapp.db`) is created automatically on first run.
- This is a basic project — features like password reset, email verification, and background jobs (Celery/Redis) were left out to keep scope manageable.

## Author

Arnav Pathela
