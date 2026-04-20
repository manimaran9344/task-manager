from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

import models, schemas
from database import SessionLocal, engine
from auth import create_access_token, verify_token

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# ✅ CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ✅ GET CURRENT USER (FIXED 🔥)
def get_current_user(Authorization: str = Header(None)):
    if Authorization is None:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        token = Authorization.split(" ")[1]
        payload = verify_token(token)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        return payload["user_id"]

    except:
        raise HTTPException(status_code=401, detail="Invalid Authorization format")


# 🏠 Home
@app.get("/")
def home():
    return {"message": "API is running"}


@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # ✅ check if user exists
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = models.User(
        username=user.username,
        password=user.password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User registered successfully"}


# 🔐 Login
@app.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"user_id": db_user.id})
    return {"access_token": token}


# 📋 Get Tasks (PROTECTED)
@app.get("/tasks", response_model=list[schemas.Task])
def get_tasks(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()


# ➕ Create Task (PROTECTED)
@app.post("/tasks", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    new_task = models.Task(
        title=task.title,
        completed=False,
        user_id=user_id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


# ✅ Complete Task (PROTECTED)
@app.put("/tasks/{task_id}")
def complete_task(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.completed = True
    db.commit()
    return {"message": "Task completed"}


# ❌ Delete Task (PROTECTED)
@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.user_id == user_id
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}