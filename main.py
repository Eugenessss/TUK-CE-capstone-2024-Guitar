from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User  # User 모델이 정의된 경우

app = FastAPI()

# 의존성: 데이터베이스 연결
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 데이터 추가 API
@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    user = User(name=name, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# 데이터 조회 API
@app.get("/users/")
def read_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI!"}

