# schemas.py

from pydantic import BaseModel
from typing import List

class InterestTag(BaseModel):
    name: str
    class Config:
        from_attributes = True

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

class Career(BaseModel):
    id: int
    title: str
    description: str
    interest_tags: List[InterestTag] = []
    class Config:
        from_attributes = True
        
class ConversationalInput(BaseModel):
    conversation_history: List[dict]
    user_age: str
    hobbies: List[str]