# Task Manager App

A simple full stack task manager app made using Flask and VueJS. Made this as part of app dev placement prep activity.

## Features

- Register / Login with email and password
- Token based authentication (using Flask-Security)
- Add, view, update (mark done), delete tasks
- Each user only sees their own tasks
- Set priority for tasks (low/medium/high)

## Tech Stack

- Backend: Flask, Flask-SQLAlchemy, Flask-Security-Too
- Frontend: VueJS (CDN, no build step), Axios
- DB: SQLite

## Installation

### Backend

```
cd backend
pip install -r requirements.txt
python app.py
```

Server runs on http://127.0.0.1:5000

### Frontend

Just open `frontend/index.html` in your browser. No build steps needed since Vue and Axios are loaded from CDN.

(if you get CORS errors trying to open the file directly, run a simple server like `python -m http.server 8000` inside the frontend folder and open localhost:8000)

## API Documentation

### POST /api/register
Body: `{ "email": "...", "password": "..." }`
Creates a new user.

### POST /api/login
Body: `{ "email": "...", "password": "..." }`
Returns `{ "token": "...", "email": "...", "user_id": ... }`

All routes below need header: `Authentication-Token: <token>`

### GET /api/tasks
Returns list of tasks for logged in user.

### POST /api/tasks
Body: `{ "title": "...", "desc": "...", "priority": "low/medium/high" }`
Adds a new task.

### PUT /api/tasks/<id>
Body: any of `title`, `desc`, `done`, `priority`
Updates a task.

### DELETE /api/tasks/<id>
Deletes a task.

## Notes

- db file (taskapp.db) gets created automatically first time you run the app
- this is a basic project, didn't add things like password reset / email confirmation etc
