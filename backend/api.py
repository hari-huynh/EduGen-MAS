import uvicorn
import uuid

from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database.schema import SessionLocal, ProjectSchema, SessionSchema, UserSchema, BookSchema
from sqlalchemy.orm import Session
import json
from typing import List
from datetime import datetime

from agents.pydantic_models import CurriculumResult
from presentation.classroom_ops import ClassroomMaterial, classroom_create_course, classroom_create_topic, classroom_create_coursework_material
# from database import SessionLocal, User


## Data Base
from urllib.parse import quote_plus
from pymongo.mongo_client import MongoClient
# from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo.server_api import ServerApi
# from data.unstructured_utils import chunk_data, save_image, chunk_text
from data.newdata import split_markdown_by_title
from data.huggingFace_utils import embedding
from data.vectorDB import setup_vector_store
db_password = quote_plus("Truong2003@")

uri = f"mongodb+srv://quangtruongairline:{db_password}@chatbotdb.pzsqjdr.mongodb.net/?retryWrites=true&w=majority&appName=chatbotdb"

# Create a new client and connect to the server
client = MongoClient(uri,tls=True, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

mongodb = client.get_database('chatbotdb')

# mongo_memory = MongoDBSaver(db)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Project(BaseModel):
    id: str
    name: str
    create_at: str
    
class ChatSession(BaseModel):
    id: str
    name: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@app.get("/projects", response_model=List[Project])
def get_projects(userId: str = Query(...), db: Session = Depends(get_db)):
    try:
        projects = db.query(ProjectSchema).filter(ProjectSchema.creator_id == userId).all()

        if projects:
            return [
                Project(id = pr.project_id, name = pr.name, create_at = str(pr.create_at))
                for pr in projects
            ]
        else:
            return []
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


class ProjectInfo(BaseModel):
    name: str
    creator_id: str


@app.get("/sessions", response_model=List[ChatSession])
def get_sessions(userId: str = Query(...), projectId: str =Query(...), db: Session = Depends(get_db)):
    try:
        sessions = db.query(SessionSchema).filter(SessionSchema.user_id == userId,
                                                  SessionSchema.project_id == projectId).all()

        if sessions:
            return [
                ChatSession(id = sess.session_id, name = sess.session_id)
                for sess in sessions
            ]
        else:
            return []
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))





@app.post("/add_new_project")
def add_new_project(new_project: ProjectInfo, db: Session = Depends(get_db)):
    try:
        new_project_id = str(uuid.uuid4())
        new_session_id = str(uuid.uuid4())

        project = ProjectSchema(
            project_id = new_project_id,
            name = new_project.name,
            creator_id = new_project.creator_id,
            book_cover = None,
            create_at = datetime.now()
        )

        session = SessionSchema(
            session_id = new_session_id,
            project_id = new_project_id,
            user_id = new_project.creator_id
        )

        db.add(project)        
        db.add(session)
        db.commit()
        
        db.refresh(project)
        db.refresh(session)

        return {"message": "User registered successfully",
                "projectId": new_project_id,
                "sessionId": new_session_id }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


class NewSession(BaseModel):
    id: str
    user_id: str
    project_id: str
@app.post("/add_new_session")
def add_new_session(new_session: NewSession, db: Session = Depends(get_db)):
    try:
        new_session_id = str(uuid.uuid4())
        
        session = SessionSchema(
            session_id = new_session_id,
            project_id = new_session.project_id,
            user_id = new_session.user_id
        )
        db.add(session)
        db.commit()
        db.refresh(session)
        
        return {
            "message": "Session created successfully",
            "session_id": new_session_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


class Book(BaseModel):
    book_id: str
    link_book: str
    user_id: str
    project_id: str
    name_book:str
    

@app.post("/add_new_book")
def add_new_session(book: Book, db: Session = Depends(get_db)):
    try:
        new_book_id = str(uuid.uuid4())
        
        newBook = BookSchema(
            book_id = new_book_id,
            project_id = book.project_id,
            user_id = book.user_id,
            link_book=book.link_book,
            name_book= book.name_book
        )
        db.add(newBook)
        db.commit()
        db.refresh(newBook)
        
        return {
            "message": "Book created successfully",
            "session_id": new_book_id
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/get_book", response_model=List[Book])
def get_book(userId: str = Query(...), projectId: str =Query(...), db: Session = Depends(get_db)):
    try:
        books = db.query(BookSchema).filter(BookSchema.user_id == userId,
                                                  BookSchema.project_id == projectId).all()

        
        if books:
            return [
                {
                    "book_id": book.book_id,
                    "user_id": book.user_id,
                    "project_id": book.project_id,
                    "name_book": book.name_book,  
                    "link_book": book.link_book
                }
                for book in books
            ]
        else:
            return []
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



class UserCreate(BaseModel):
    user_id: str
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


@app.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(UserSchema).filter_by(user_id=user.user_id).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        db_user = UserSchema(
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


@app.get("/messages")
def get_messages_history(sessionId: str):
    # print(sessionId)
    messages = mongodb["chatbotdb"].find_one({"session_id": sessionId})
    
    if messages:
        return messages.get("messages")
    else:
        return []
    
@app.get("/get_session_info")
def get_session_info(sessionId: str):
    session_info = mongodb["chatbotdb"].find_one({"session_id": sessionId}) 
    if session_info:
        return session_info.get("state")
    else:
        return []
        
        

class FileInfo(BaseModel):
    file_url: str
    file_name: str
    
class Message(BaseModel):
    session_id: str
    role: str
    content: str
    timestamp: str    
    
@app.post("/save_message")
def get_messages_history(mess: Message ):
    
    mongodb["chatbotdb"].update_one(
        { "session_id": mess.session_id},
        {
            "$push": { 
                "messages": {
                    "content": mess.content,
                    "role": mess.role,
                    "timestamp": mess.timestamp
                },
            }
        },
        upsert=True
    )
    

    
@app.post("/api/handle_uploaded_pdf")
async def handle_uploaded_pdf(file_info: FileInfo):
    print(f"📄 Received PDF: {file_info.file_name}")
    print(f"🌐 URL: {file_info.file_url}")

@app.post("/extract")
async def processing(path_file):

    chunks=split_markdown_by_title(filepath=path_file)
    
    embedddings=embedding()
    setup_vector_store(chunks, embedddings)
    print("SAVE DB")


class LearningMaterial(BaseModel):
    curriculum: CurriculumResult
    lecture_urls: List[str]
    presentation_urls: List[str]
    quiz_urls: List[str]


@app.post("/export/classroom")
def export_to_classroom(materials: LearningMaterial):
    curriculum = materials.curriculum
    name = curriculum.title
    description = curriculum.overview
    titles = [mod.title for mod in curriculum.modules]
    
    # Create a new course
    course_id = classroom_create_course(name, description)
    
    # Create topic and upload file base on urls
    for idx, title in enumerate(titles):
        topic_id = classroom_create_topic(course_id, title)


        # Upload lecture note
        classroom_materials = [
            ClassroomMaterial(url = materials.lecture_urls[idx], title = f"[LECTURE-NOTE] {title}")
        ]

        classroom_create_coursework_material(course_id, f"[LECTURE-NOTE] {title}", "", classroom_materials, topic_id)


        # Upload quizzes
        classroom_materials = [
            ClassroomMaterial(url = materials.quiz_urls[idx], title = f"[QUIZ] {title}")
        ]

        classroom_create_coursework_material(course_id, f"[QUIZ] {title}", "", classroom_materials, topic_id)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)