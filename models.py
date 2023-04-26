from sqlalchemy import String, Integer, Column, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from flask_login import UserMixin

Base = declarative_base()


class AppUser(Base, UserMixin):
    __tablename__ = "appuser"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(30), unique=True)
    password = Column(String(64))
    careers = relationship("Career", backref="appuser", lazy=True, cascade="all, delete-orphan" )

class Career(Base):
    __tablename__ = "career"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(String(128))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('appuser.id', ondelete='CASCADE'),  nullable=False)
    
