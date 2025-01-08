from fastapi import FastAPI, HTTPException
import firebase_admin
from firebase_admin import credentials, firestore

# FastAPI 앱 생성
app = FastAPI()

# Firebase Admin SDK 초기화
cred = credentials.Certificate("firebase-key.json")  # Firebase 키 파일 경로
firebase_admin.initialize_app(cred)

# Firestore 클라이언트 생성
db = firestore.client()

@app.get("/")
async def root():
    return {"message": "Firebase and FastAPI are connected!"}

@app.post("/add-user/")
async def add_user(user_id: str, name: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user_ref.set({"name": name})
        return {"message": f"User {name} added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get-user/{user_id}")
async def get_user(user_id: str):
    try:
        user_ref = db.collection("users").document(user_id)
        user = user_ref.get()
        if not user.exists:
            raise HTTPException(status_code=404, detail="User not found")
        return user.to_dict()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

