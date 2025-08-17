# main.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
import traceback
import json
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

import models, schemas
from database import SessionLocal, engine

# --- AI SETUP ---
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemma-3n-e4b-it')

# --- DATABASE AND APP SETUP ---
models.Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ENDPOINTS ---
@app.get("/__secret_seed_command__")
def secret_seed(db: Session = Depends(get_db)):
    if db.query(models.Quiz).first():
        return {"message": "Database already seeded."}
    try:
        # The full seeding logic from your seed.py file goes here
        # ...
        return {"message": "Database seeded successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).options(
        joinedload(models.Quiz.questions)
        .joinedload(models.Question.choices)
        .joinedload(models.Choice.interest_tags)
    ).filter(models.Quiz.id == quiz_id).first()
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@app.post("/generate-conversational-question")
def generate_conversational_question(convo_input: schemas.ConversationalInput):
    history = convo_input.conversation_history
    user_age = convo_input.user_age
    hobbies = ", ".join(convo_input.hobbies)
    history_string = "\n".join([f"Q: {turn['question']}\nA: {turn['answer']}" for turn in history])
    
    prompt = f"""
    You are "Zhero," an AI career counselor creating a personalized MCQ quiz for a '{user_age}' whose hobbies include '{hobbies}'.
    Based on the conversation history, generate the VERY NEXT question.
    --- CONVERSATION HISTORY ---
    {history_string}
    --- END OF HISTORY ---
    ## RULES:
    1.  ANALYZE & DEEPEN: Analyze the history to identify emerging interests. Generate a new question that probes deeper into ONE of these interests.
    2.  CREATE A SCENARIO: The question must be a specific, age-appropriate scenario.
    3.  GENERATE 4 OPTIONS: Create four distinct, plausible answer options.
    4.  TAG EACH OPTION: Each option MUST be tagged with one of: ["Analytical & Investigative", "Artistic & Creative", "Social & Helping", "Enterprising & Leading", "Conventional & Organizing", "Realistic & Hands-On"].
    5.  OUTPUT FORMAT: Respond with a valid JSON object with keys "question" (string) and "choices" (list of dicts). Each choice dict must have keys "text" and "tag".
    ## EXAMPLE OUTPUT:
    {{
      "question": "A community project to build a new park is announced. What role excites you?",
      "choices": [
        {{"text": "Researching the best local plants...", "tag": "Analytical & Investigative"}},
        {{"text": "Designing a beautiful sculpture...", "tag": "Artistic & Creative"}},
        {{"text": "Organizing volunteer schedules...", "tag": "Social & Helping"}},
        {{"text": "Building the benches and planting trees...", "tag": "Realistic & Hands-On"}}
      ]
    }}
    Generate the JSON for the next question now.
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An exception occurred: {repr(e)}")

@app.post("/generate-ai-recommendations")
def generate_ai_recommendations(convo_input: schemas.ConversationalInput):
    history = convo_input.conversation_history
    user_age = convo_input.user_age
    hobbies = ", ".join(convo_input.hobbies)
    history_string = "\n".join([f"Q: {turn['question']}\nA: {turn['answer']}" for turn in history])

    prompt = f"""
    You are "Zhero," a world-class AI career analyst reviewing an interview with a user who is '{user_age}' and has hobbies like '{hobbies}'.
    --- FULL INTERVIEW TRANSCRIPT ---
    {history_string}
    --- END TRANSCRIPT ---
    ## RULES:
    1.  HOLISTIC ANALYSIS: Analyze the conversation to identify core interests, skills, and personality traits.
    2.  DYNAMIC RECOMMENDATIONS: Suggest 3 to 5 specific career paths or fields of study relevant to the user's unique responses and age.
    3.  PERSONALIZED REASONING: For each career, provide a "Why it's a good fit for you:" section that directly references the user's answers.
    4.  OUTPUT FORMAT: Respond with a valid JSON object with a single key "recommendations", which is a list of dicts. Each dict must have keys "career" and "reason".
    ## EXAMPLE OUTPUT:
    {{
      "recommendations": [
        {{"career": "Urban Planner", "reason": "Why it's a good fit for you: Your detailed answer about designing a community park showed a passion for both creative design and analytical thinking..."}}
      ]
    }}
    Generate the JSON analysis and recommendations now.
    """
    try:
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An exception occurred: {repr(e)}")