from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage
CORS(app)

# File Paths
JOB_SKILLS_PATH = "./data/job_skills.csv"
SKILL_ASSESSMENT_PATH = "./data/skill_assessment.csv"

# Load datasets
job_skills_data = pd.read_csv(JOB_SKILLS_PATH)
skill_assessment_data = pd.read_csv(SKILL_ASSESSMENT_PATH)

# Load NLP model
sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Store user progress in session
user_sessions = {}

# Start assessment and send the first question
@app.route('/start_assessment', methods=['POST'])
def start_assessment():
    data = request.json
    job_role = data.get("job_role", "").strip().lower()

    column_name = "job_role" if "job_role" in skill_assessment_data.columns else "Job Role"

    # Get questions for the job role
    questions_df = skill_assessment_data[skill_assessment_data[column_name].str.lower() == job_role]

    if questions_df.empty:
        return jsonify({"error": f"No questions found for job role '{job_role}'"}), 404

    # Convert questions to list with options for MCQs
    questions = questions_df[['Question', 'Answer', 'Type', 'Options']].to_dict(orient="records")

    # Shuffle questions for randomness
    random.shuffle(questions)

    # Store session data (user's progress)
    user_sessions[job_role] = {
        "questions": questions,
        "current_index": 0,
        "correct_answers": 0,
        "total_questions": len(questions)
    }

    # Send first question
    first_question = questions[0]

    return jsonify({
        "question": first_question["Question"],
        "question_type": first_question["Type"],
        "options": first_question["Options"].split(",") if first_question["Type"] == "mcq" else None,
        "index": 0,
        "total_questions": len(questions)
    })

# Submit answer and get next question
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    job_role = data.get("job_role", "").strip().lower()
    user_answer = data.get("answer", "").strip()

    if job_role not in user_sessions:
        return jsonify({"error": "Assessment not started. Please start again."}), 400

    session_data = user_sessions[job_role]
    current_index = session_data["current_index"]
    questions = session_data["questions"]

    question_data = questions[current_index]
    correct_answer = question_data["Answer"].strip().lower()
    question_type = question_data["Type"]

    # MCQ: Direct answer matching
    if question_type == "mcq":
        is_correct = user_answer.lower() == correct_answer.lower()

    # Open-Ended: Use NLP similarity
    elif question_type == "open-ended":
        user_embedding = sentence_model.encode([user_answer])
        correct_embedding = sentence_model.encode([correct_answer])
        similarity = cosine_similarity(user_embedding, correct_embedding)[0][0]
        is_correct = similarity > 0.75

    # Coding: Placeholder for logic validation
    elif question_type == "coding":
        is_correct = user_answer.strip().lower() == correct_answer

    # Track correct answers
    if is_correct:
        session_data["correct_answers"] += 1

    session_data["current_index"] += 1

    # If more questions remain, send the next question
    if session_data["current_index"] < session_data["total_questions"]:
        next_question = questions[session_data["current_index"]]
        return jsonify({
            "next_question": next_question["Question"],
            "question_type": next_question["Type"],
            "options": next_question["Options"].split(",") if next_question["Type"] == "mcq" else None,
            "index": session_data["current_index"]
        })

    # Final Score Calculation
    final_score = (session_data["correct_answers"] / session_data["total_questions"]) * 100

    # Determine skill level
    if final_score < 30:
        skill_level = "Beginner"
        recommendation = "Practice basic concepts and revisit foundational skills."
    elif 30 <= final_score < 50:
        skill_level = "Intermediate"
        recommendation = "Work on projects and improve problem-solving skills."
    elif 50 <= final_score < 80:
        skill_level = "Advanced Intermediate"
        recommendation = "Learn advanced topics and contribute to open-source projects."
    else:
        skill_level = "Expert"
        recommendation = "You’ve demonstrated a high level of skill and knowledge. Keep pushing boundaries, learning new technologies, and contributing to the tech community! 🚀🔥"

    del user_sessions[job_role]

    return jsonify({
        "final_score": final_score,
        "skill_level": skill_level,
        "recommendation": recommendation
    })

# Root route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the AI-Powered Skill Assessment API!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)