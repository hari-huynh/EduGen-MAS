import os

from dotenv import load_dotenv

from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm import sessionmaker


# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    create_at = Column(DateTime)
    # projects = relationship("Project", back_populates="creator")

class Project(Base):
    __tablename__= "projects"
    project_id= Column(String, primary_key=True)
    name= Column(String)
    book_cover= Column(String)
    create_at = Column(DateTime)
    creator_id = Column(String, ForeignKey('users.user_id'))  
    # creator = relationship("User", back_populates="projects")
    



class Session(Base):
    __tablename__ = "sessions"
    session_id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    project_id = Column(String, ForeignKey("projects.project_id"))
    

Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

# truong = User(first_name="Truong", last_name="Nguyen")
# session.add(truong)
session.commit()

# res = session.query(User).all()
# print(res)
