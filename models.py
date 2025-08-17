# models.py (Corrected Version)

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base # <--- THIS LINE IS NOW FIXED

# This is an "association table" for the many-to-many relationship
# between Choices and InterestTags.
choice_interest_tag_association = Table('choice_interest_tag', Base.metadata,
    Column('choice_id', Integer, ForeignKey('choices.id')),
    Column('interest_tag_id', Integer, ForeignKey('interest_tags.id'))
)
# This is the new association table to add in models.py
career_interest_tag_association = Table('career_interest_tag', Base.metadata,
    Column('career_id', Integer, ForeignKey('careers.id')),
    Column('interest_tag_id', Integer, ForeignKey('interest_tags.id'))
)

class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    questions = relationship("Question", back_populates="quiz")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    quiz = relationship("Quiz", back_populates="questions")
    choices = relationship("Choice", back_populates="question")

class Choice(Base):
    __tablename__ = "choices"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    question_id = Column(Integer, ForeignKey("questions.id"))
    question = relationship("Question", back_populates="choices")
    # A choice can be linked to many interest tags
    interest_tags = relationship("InterestTag", secondary=choice_interest_tag_association)

class InterestTag(Base):
    __tablename__ = "interest_tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True) # e.g., "Creative", "Analytical"

    # This is the new Career class to add at the end of models.py

class Career(Base):
    __tablename__ = "careers"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)
    # A career can be linked to many interest tags
    interest_tags = relationship("InterestTag", secondary=career_interest_tag_association)