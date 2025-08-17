# schemas.py

from pydantic import BaseModel
from typing import List, Optional

class InterestTag(BaseModel):
    name: str
    class Config:
        from_attributes = True

# This is the corrected Choice schema in schemas.py
class Choice(BaseModel):
    id: int
    text: str
    interest_tags: List[InterestTag] = [] 
    class Config:
        from_attributes = True

class Question(BaseModel):
    id: int
    text: str
    choices: List[Choice] = []
    class Config:
        from_attributes = True

class Quiz(BaseModel):
    id: int
    title: str
    description: str
    questions: List[Question] = []
    class Config:
        from_attributes = True

# Schema for a user submitting a single answer
class UserResponse(BaseModel):
    question_id: int
    choice_id: int

    # Add this new class to the end of schemas.py

class Career(BaseModel):
    id: int
    title: str
    description: str
    interest_tags: List[InterestTag] = []
    
    class Config:
        from_attributes = True