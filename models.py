from enum import Enum as Enums
from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from flask_login import UserMixin

Base = declarative_base()
class Category(Enums):
    SCIENCES = 'SCIENCE'
    COMMERCE = 'COMMERCE'
    ARTS = 'ARTS'


class AppUser(Base, UserMixin):
    __tablename__ = "appuser"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(30), unique=True)
    password = Column(String(64))

class Career(Base):
    __tablename__ = "career"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50))
    description = Column(String(128))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    picture_url=Column(String())
    status = Column(Enum(Category), nullable=False)
    courses = relationship("Courses", backref="career", lazy=False, cascade="all, delete-orphan" )
    
class Courses(Base):
    __tablename__ = "courses"   
    id = Column(Integer, primary_key=True, autoincrement=True)
    course_name = Column(String(50))
    career_id = Column(Integer, ForeignKey('career.id'), nullable=False)
    subjects = relationship("Subjects", backref="courses", lazy=False, cascade="all, delete-orphan" )
    

class Subjects(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    course_id= Column(Integer, ForeignKey("courses.id"), nullable=False)
    


