from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Create the database engine
DATABASE_URL = "sqlite:///./courses.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class
Base = declarative_base()

# Define the Course model
class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)

# Create the courses table
Base.metadata.create_all(bind=engine)

# Create FastAPI instance
app = FastAPI()

# Pydantic model for the request body
class CourseCreate(BaseModel):
    name: str
    description: str

# POST endpoint to add a new software course
@app.post("/courses", response_model=dict)
def add_course(course: CourseCreate):
    db = SessionLocal()
    new_course = Course(name=course.name, description=course.description)
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    db.close()
    return {"message": "Course added successfully"}

# GET endpoint to retrieve the list of all courses
@app.get("/courses", response_model=List[CourseCreate])
def get_courses():
    db = SessionLocal()
    courses = db.query(Course).all()
    print("Courses fetched:", courses)  # Debugging statement
    db.close()
    return courses
