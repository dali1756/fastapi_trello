from sqlalchemy import Column, Integer, Text, String, DateTime
from db.db import BaseModel

class Project(BaseModel):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
