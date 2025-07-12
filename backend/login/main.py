from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from database import session, User
from database import SessionLocal, User
from sqlalchemy.orm import Session


from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
class UserCreate(BaseModel):
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    
# class UserCreate(BaseModel):
#     user_id: str
#     first_name: str
#     last_name: str
#     email: str

# @app.post("/register")
# def register_user(user: UserCreate):
#     existing_user = session.query(User).filter_by(user_id=user.user_id).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="User already exists")
#     db_user = User(
#         user_id=user.user_id, 
#         first_name=user.first_name,
#         last_name=user.last_name,
#         email=user.email,
#         create_at=datetime.utcnow()
#     )
#     session.add(db_user)
#     session.commit()
#     return {"message": "User registered successfully"}

@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter_by(user_id=user.user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        db_user = User(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            create_at=datetime.utcnow()
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))