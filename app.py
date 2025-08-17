# app.py

import streamlit as st
import requests
import json

# --- Page Configuration & Title ---
st.set_page_config(page_title="Project Zhero", page_icon="🚀", layout="centered")
st.title("Project Zhero 🚀")

# --- Backend API URL ---
BACKEND_URL = st.secrets.get("BACKEND_URL", "http://127.0.0.1:8000")

# --- Initialize Session State ---
if 'stage' not in st.session_state:
    st.session_state.stage = 'setup'
if 'user_age' not in st.session_state:
    st.session_state.user_age = ""
if 'hobbies' not in st.session_state:
    st.session_state.hobbies = ""
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 5
if 'static_quiz_data' not in st.session_state:
    st.session_state.static_quiz_data = None
if 'current_q_index' not in st.session_state:
    st.session_state.current_q_index = 0
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_question_obj' not in st.session_state:
    st.session_state.current_question_obj = {}
if 'career_recommendations' not in st.session_state:
    st.session_state.career_recommendations = []

# --- Functions (Callbacks) ---

def start_quiz():
    try:
        response = requests.get(f"{BACKEND_URL}/quizzes/1")
        response.raise_for_status()
        st.session_state.static_quiz_data = response.json()['questions']
        st.session_state.stage = 'quiz'
        st.session_state.current_q_index = 0
        st.session_state.conversation_history = []
        st.session_state.current_question_obj = st.session_state.static_quiz_data[0]
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the backend: {e}. Please ensure the backend is running and accessible.")
        st.session_state.stage = 'error'

def handle_answer(question_text, answer_text):
    st.session_state.conversation_history.append({"question": question_text, "answer": answer_text})
    
    current_question_number = st.session_state.current_q_index + 1
    
    if current_question_number < len(st.session_state.static_quiz_data):
        st.session_state.current_q_index += 1
        st.session_state.current_question_obj = st.session_state.static_quiz_data[st.session_state.current_q_index]
    elif current_question_number < st.session_state.total_questions:
        with st.spinner("Your personal AI counselor is thinking..."):
            try:
                request_body = {
                    "conversation_history": st.session_state.conversation_history,
                    "user_age": st.session_state.user_age,
                    "hobbies": [h.strip() for h in st.session_state.hobbies.split(',') if h.strip()]
                }
                response = requests.post(f"{BACKEND_URL}/generate-conversational-question", json=request_body)
                response.raise_for_status()
                st.session_state.current_question_obj = response.json()
                st.session_state.current_q_index += 1
            except requests.exceptions.RequestException as e:
                st.error(f"Error generating AI question: {e}")
                st.session_state.stage = 'error'
    else:
        st.session_state.stage = 'final_analysis'

def run_final_analysis_and_get_recs():
    with st.spinner("Analyzing your conversation and generating recommendations..."):
        try:
            request_body = {
                "conversation_history": st.session_state.conversation_history,
                "user_age": st.session_state.user_age,
                "hobbies": [h.strip() for h in st.session_state.hobbies.split(',') if h.strip()]
            }
            response = requests.post(f"{BACKEND_URL}/generate-ai-recommendations", json=request_body)
            response.raise_for_status()
            st.session_state.career_recommendations = response.json().get('recommendations', [])
            st.session_state.stage = 'show_recommendations'
        except requests.exceptions.RequestException as e:
            st.error(f"Error getting AI recommendations: {e}")
            st.session_state.stage = 'final_analysis'

# --- UI Rendering ---

if st.session_state.stage == 'setup':
    st.subheader("First, let's personalize your session.")
    st.session_state.user_age = st.text_input("What is your age or grade level?", placeholder="e.g., 10 years old")
    st.session_state.hobbies = st.text_input("List a few hobbies or interests (optional)", placeholder="e.g., video games, painting")
    st.session_state.total_questions = st.selectbox("Select Quiz Length:", [5, 10, 20], index=0, format_func=lambda x: f"{x} Questions")
    st.button("Start Analysis", on_click=start_quiz)

elif st.session_state.stage == 'quiz':
    question_num = st.session_state.current_q_index + 1
    total_q = st.session_state.total_questions
    st.progress((question_num - 1) / total_q, text=f"Question {question_num} of {total_q}")
    question_text = st.session_state.current_question_obj.get('question', st.session_state.current_question_obj.get('text', ''))
    st.subheader(question_text)
    st.write("---")
    for i, choice in enumerate(st.session_state.current_question_obj['choices']):
        answer_text = choice.get('text', '')
        if 'tag' in choice:
            answer_text = f"{choice['text']} ({choice['tag']})"
        st.button(choice['text'], key=i, on_click=handle_answer, args=(question_text, answer_text))

elif st.session_state.stage == 'final_analysis':
    st.success("Analysis Complete!")
    st.info("Based on your conversation, we're now ready to discover your personalized career recommendations.")
    st.button("Show My AI Recommendations", on_click=run_final_analysis_and_get_recs)

elif st.session_state.stage == 'show_recommendations':
    st.success("Here are your personalized AI-generated recommendations!")
    st.write("---")
    if st.session_state.career_recommendations:
        for career in st.session_state.career_recommendations:
            with st.container(border=True):
                st.subheader(career.get('career', 'N/A'))
                st.markdown(f"**Why it's a good fit for you:** {career.get('reason', 'No reason provided.')}")
    else:
        st.warning("The AI could not generate specific career recommendations. Try a 'Deep Dive' quiz for more accuracy!")
    st.write("---")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

elif st.session_state.stage == 'error':
    st.error("Something went wrong with the connection to our AI. Please ensure the backend is running.")
    if st.button("Start Over"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()