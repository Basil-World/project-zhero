# seed.py (New "Universal Interests" Version)

from database import SessionLocal, engine
from models import Quiz, Question, Choice, InterestTag, Career, Base, choice_interest_tag_association, career_interest_tag_association

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        print("Starting to seed the database...")

        # Clear old data
        db.execute(choice_interest_tag_association.delete())
        db.execute(career_interest_tag_association.delete())
        db.query(Career).delete()
        db.query(InterestTag).delete()
        db.query(Choice).delete()
        db.query(Question).delete()
        db.query(Quiz).delete()
        db.commit()

        # --- NEW, BROADER INTEREST TAGS ---
        print("Creating universal interest tags...")
        tag_analytical = InterestTag(name="Analytical & Investigative") # Science, Research, Data
        tag_creative = InterestTag(name="Artistic & Creative") # Arts, Design, Writing
        tag_social = InterestTag(name="Social & Helping") # Healthcare, Teaching, Social Work
        tag_enterprising = InterestTag(name="Enterprising & Leading") # Business, Law, Administration
        tag_conventional = InterestTag(name="Conventional & Organizing") # Finance, Admin, Logistics
        tag_realistic = InterestTag(name="Realistic & Hands-On") # Engineering, Sports, Trades
        db.add_all([tag_analytical, tag_creative, tag_social, tag_enterprising, tag_conventional, tag_realistic])
        db.commit()

        # --- NEW, MORE GENERIC INITIAL QUIZ ---
        print("Creating universal quiz...")
        quiz1 = Quiz(title="Discover Your Core Interests", description="A few questions to understand what drives you.")
        db.add(quiz1)
        db.commit()

        # Question 1: How do you prefer to solve problems?
        q1 = Question(text="When faced with a complex problem, what is your first instinct?", quiz_id=quiz1.id)
        db.add(q1)
        db.commit()
        db.add_all([
            Choice(text="Analyze data and research to find a logical solution.", question_id=q1.id, interest_tags=[tag_analytical]),
            Choice(text="Brainstorm unconventional ideas and create something new.", question_id=q1.id, interest_tags=[tag_creative]),
            Choice(text="Organize a team and delegate tasks to get it done efficiently.", question_id=q1.id, interest_tags=[tag_enterprising]),
            Choice(text="Build a physical prototype or take direct, hands-on action.", question_id=q1.id, interest_tags=[tag_realistic]),
        ])

        # Question 2: What kind of work environment energizes you?
        q2 = Question(text="Which of these work environments sounds most appealing?", quiz_id=quiz1.id)
        db.add(q2)
        db.commit()
        db.add_all([
            Choice(text="A quiet library or lab, focused on deep thinking and discovery.", question_id=q2.id, interest_tags=[tag_analytical]),
            Choice(text="A bustling studio or workshop, surrounded by creativity and expression.", question_id=q2.id, interest_tags=[tag_creative]),
            Choice(text="A collaborative office or field site, helping and interacting with people.", question_id=q2.id, interest_tags=[tag_social]),
            Choice(text="A well-structured office, focused on order, accuracy, and process.", question_id=q2.id, interest_tags=[tag_conventional]),
        ])
        
        # Question 3: What gives you the greatest sense of accomplishment?
        q3 = Question(text="What brings you the greatest sense of accomplishment?", quiz_id=quiz1.id)
        db.add(q3)
        db.commit()
        db.add_all([
            Choice(text="Solving a difficult puzzle or discovering a new piece of knowledge.", question_id=q3.id, interest_tags=[tag_analytical]),
            Choice(text="Making a positive impact on someone's life or community.", question_id=q3.id, interest_tags=[tag_social]),
            Choice(text="Leading a team to victory or successfully launching a new venture.", question_id=q3.id, interest_tags=[tag_enterprising]),
            Choice(text="Creating a detailed plan and executing it flawlessly.", question_id=q3.id, interest_tags=[tag_conventional]),
        ])
        db.commit()

        # --- NEW, MORE DIVERSE CAREERS ---
        print("Creating diverse careers...")
        db.add_all([
            Career(title="Doctor / Nurse", description="...", interest_tags=[tag_social, tag_analytical]),
            Career(title="Mechanical Engineer", description="...", interest_tags=[tag_realistic, tag_analytical]),
            Career(title="Lawyer", description="...", interest_tags=[tag_enterprising, tag_analytical]),
            Career(title="Artist / Illustrator", description="...", interest_tags=[tag_creative]),
            Career(title="Marine Biologist", description="...", interest_tags=[tag_analytical, tag_realistic]),
            Career(title="Accountant", description="...", interest_tags=[tag_conventional, tag_analytical]),
            Career(title="Professional Athlete / Coach", description="...", interest_tags=[tag_realistic]),
            Career(title="Civil Servant / Administrator", description="...", interest_tags=[tag_conventional, tag_enterprising]),
            Career(title="Entrepreneur", description="...", interest_tags=[tag_enterprising, tag_creative]),
        ])
        db.commit()

        print("Database seeded successfully!")
    except Exception as e:
        print(f"An error occurred during seeding: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    seed_database()