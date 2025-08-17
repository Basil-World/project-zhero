# main.py (Final Version with Seeding Endpoint)

import os
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
import json
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

# Import our other files
import models, schemas
from database import SessionLocal, engine

# --- AI SETUP ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')

# --- DATABASE AND APP SETUP ---
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- THE SECRET SEEDING ENDPOINT ---
@app.get("/__secret_seed_command__")
def secret_seed(db: Session = Depends(get_db)):
    """This endpoint runs the seeding logic. It should only be run once."""
    if db.query(models.Quiz).first():
        return {"message": "Database already seeded."}
    
    try:
        # ====================================================================
        # === PASTE THE CODE YOU JUST COPIED (FROM seed.py) RIGHT HERE ===
        # ====================================================================

        # It starts with: print("Starting to seed the database...")
        # Make sure to change all model names to have "models." in front of them
        # e.g., Quiz becomes models.Quiz, Career becomes models.Career, etc.

        # I will do this for you to make it easy:

        print("Starting to seed the database...")

        # Clear old data
        db.execute(models.choice_interest_tag_association.delete())
        db.execute(models.career_interest_tag_association.delete())
        db.query(models.Career).delete()
        db.query(models.InterestTag).delete()
        db.query(models.Choice).delete()
        db.query(models.Question).delete()
        db.query(models.Quiz).delete()
        db.commit()

        # --- NEW, BROADER INTEREST TAGS ---
        print("Creating universal interest tags...")
        tag_analytical = models.InterestTag(name="Analytical & Investigative")
        tag_creative = models.InterestTag(name="Artistic & Creative")
        tag_social = models.InterestTag(name="Social & Helping")
        tag_enterprising = models.InterestTag(name="Enterprising & Leading")
        tag_conventional = models.InterestTag(name="Conventional & Organizing")
        tag_realistic = models.InterestTag(name="Realistic & Hands-On")
        db.add_all([tag_analytical, tag_creative, tag_social, tag_enterprising, tag_conventional, tag_realistic])
        db.commit()

        # --- NEW, MORE GENERIC INITIAL QUIZ ---
        print("Creating universal quiz...")
        quiz1 = models.Quiz(title="Discover Your Core Interests", description="A few questions to understand what drives you.")
        db.add(quiz1)
        db.commit()

        # Question 1
        q1 = models.Question(text="When faced with a complex problem, what is your first instinct?", quiz_id=quiz1.id)
        db.add(q1)
        db.commit()
        db.add_all([
            models.Choice(text="Analyze data and research to find a logical solution.", question_id=q1.id, interest_tags=[tag_analytical]),
            models.Choice(text="Brainstorm unconventional ideas and create something new.", question_id=q1.id, interest_tags=[tag_creative]),
            models.Choice(text="Organize a team and delegate tasks to get it done efficiently.", question_id=q1.id, interest_tags=[tag_enterprising]),
            models.Choice(text="Build a physical prototype or take direct, hands-on action.", question_id=q1.id, interest_tags=[tag_realistic]),
        ])

        # Question 2
        q2 = models.Question(text="Which of these work environments sounds most appealing?", quiz_id=quiz1.id)
        db.add(q2)
        db.commit()
        db.add_all([
            models.Choice(text="A quiet library or lab, focused on deep thinking and discovery.", question_id=q2.id, interest_tags=[tag_analytical]),
            models.Choice(text="A bustling studio or workshop, surrounded by creativity and expression.", question_id=q2.id, interest_tags=[tag_creative]),
            models.Choice(text="A collaborative office or field site, helping and interacting with people.", question_id=q2.id, interest_tags=[tag_social]),
            models.Choice(text="A well-structured office, focused on order, accuracy, and process.", question_id=q2.id, interest_tags=[tag_conventional]),
        ])
        
        # Question 3
        q3 = models.Question(text="What brings you the greatest sense of accomplishment?", quiz_id=quiz1.id)
        db.add(q3)
        db.commit()
        db.add_all([
            models.Choice(text="Solving a difficult puzzle or discovering a new piece of knowledge.", question_id=q3.id, interest_tags=[tag_analytical]),
            models.Choice(text="Making a positive impact on someone's life or community.", question_id=q3.id, interest_tags=[tag_social]),
            models.Choice(text="Leading a team to victory or successfully launching a new venture.", question_id=q3.id, interest_tags=[tag_enterprising]),
            models.Choice(text="Creating a detailed plan and executing it flawlessly.", question_id=q3.id, interest_tags=[tag_conventional]),
        ])
        db.commit()

        # --- NEW, MORE DIVERSE CAREERS ---
        print("Creating diverse careers...")
        db.add_all([
            models.Career(title="Doctor / Nurse", description="...", interest_tags=[tag_social, tag_analytical]),
            models.Career(title="Mechanical Engineer", description="...", interest_tags=[tag_realistic, tag_analytical]),
            models.Career(title="Lawyer", description="...", interest_tags=[tag_enterprising, tag_analytical]),
            models.Career(title="Artist / Illustrator", description="...", interest_tags=[tag_creative]),
            models.Career(title="Marine Biologist", description="...", interest_tags=[tag_analytical, tag_realistic]),
            models.Career(title="Accountant", description="...", interest_tags=[tag_conventional, tag_analytical]),
            models.Career(title="Professional Athlete / Coach", description="...", interest_tags=[tag_realistic]),
            models.Career(title="Civil Servant / Administrator", description="...", interest_tags=[tag_conventional, tag_enterprising]),
            models.Career(title="Entrepreneur", description="...", interest_tags=[tag_enterprising, tag_creative]),
        ])
        db.commit()

        print("Database seeded successfully!")

        # ====================================================================
        # === END OF PASTED CODE ===
        # ====================================================================

        return {"message": "Database seeded successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# --- ALL YOUR OTHER API ENDPOINTS GO HERE ---
# (read_quiz, generate_conversational_question, generate_ai_recommendations)
# These should already be in your file.