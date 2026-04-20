FastAPI Task Manager README
FastAPI Task Manager
A simple Task Management Web Application built using FastAPI, JWT authentication, and a basic frontend (HTML/CSS/Users can register, login, and manage their personal tasks securely.
FEATURES
Authentication:
- User Registration
- User Login
- JWT Token Authentication
- Password Hashing using bcrypt
Task Management:
- Create Task
- View All Tasks (user-specific)
- View Single Task
- Update Task (mark completed / edit)
- Delete Task
- Filtering by completion status
Frontend:
- Simple HTML, CSS, JavaScript UI
- Login & Registration pages
- Task dashboard
- Create, update, delete tasks
TECH STACK
- FastAPI
- SQLite
- SQLAlchemy
- JWT (python-jose)
- bcrypt
- HTML, CSS, JavaScript
HOW TO RUN LOCALLY
1️⃣ Install dependencies
pip install -r requirements.txt
2️⃣ Run the FastAPI server
uvicorn main:app --reload
3️⃣ Open API documentation
http://127.0.0.1:8000/docs
GIT
1. Clone repository:
git clone https://github.com/manimaran9344/task-manager.git
2. Create virtual environment:
python -m venv venv
Activate:
venv\Scripts\activate

API ENDPOINTS
Auth:
POST /register
POST /login
Tasks:
POST /tasks
GET /tasks
GET /tasks/{id}
PUT /tasks/{id}
DELETE /tasks/{id}
QUERY FEATURES

https://your-deployment-link.com
IMPORTANT NOTES
- Do not commit .env file
- Each user can access only their tasks
- JWT required for protected routes
AUTHOR
Mani Maran
FastAPI Developer Intern Project