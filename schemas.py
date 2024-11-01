# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BlogPost(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str
    author: str
    published_date: datetime = Field(default_factory=datetime.utcnow)

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str]
    author: Optional[str]
