from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from .database import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    summary = Column(Text)
    category = Column(String)
    created_at = Column(DateTime, server_default=func.now())
