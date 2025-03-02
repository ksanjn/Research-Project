from flask import Flask, request, jsonify, session
from flask_cors import CORS
import pandas as pd
import random
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ✅ Initialize Flask app
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Needed for session storage
CORS(app)

# ✅ File Paths
JOB_SKILLS_PATH = "./data/job_skills.csv"
SKILL_ASSESSMENT_PATH = "./data/skill_assessment.csv"

# ✅ Load datasets
job_skills_data = pd.read_csv(JOB_SKILLS_PATH)
skill_assessment_data = pd.read_csv(SKILL_ASSESSMENT_PATH)

# ✅ Load NLP model
sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# ✅ Store user progress in session
user_sessions = {}

# ✅ Start assessment and send the first question
@app.route('/start_assessment', methods=['POST'])
def start_assessment():
    data = request.json
    job_role = data.get("job_role", "").strip().lower()

    # Fix column name dynamically
    column_name = "job_role" if "job_role" in skill_assessment_data.columns else "Job Role"

    # Get questions for the given job role
    questions_df = skill_assessment_data[skill_assessment_data[column_name].str.lower() == job_role]

    if questions_df.empty:
        return jsonify({"error": f"No questions found for job role '{job_role}'"}), 404

    # Convert questions to list
    questions = questions_df[['Question', 'Answer']].to_dict(orient="records")
    total_questions = len(questions)

    # Shuffle questions for randomness
    random.shuffle(questions)

    # Store session data (user's progress)
    user_sessions[job_role] = {
        "questions": questions,
        "current_index": 0,
        "correct_answers": 0,
        "total_questions": total_questions
    }

    # Send first question
    first_question = questions[0]["Question"]

    return jsonify({
        "question": first_question,
        "index": 0,
        "total_questions": total_questions
    })

# ✅ Submit answer and get next question
@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.json
    job_role = data.get("job_role", "").strip().lower()
    user_answer = data.get("answer", "").strip()

    if job_role not in user_sessions:
        return jsonify({"error": "Assessment not started. Please start again."}), 400

    # Get session data
    session_data = user_sessions[job_role]
    current_index = session_data["current_index"]
    questions = session_data["questions"]

    # Get correct answer
    correct_answer = questions[current_index]["Answer"].strip().lower()

    # Compute similarity
    user_embedding = sentence_model.encode([user_answer])
    correct_embedding = sentence_model.encode([correct_answer])
    similarity = cosine_similarity(user_embedding, correct_embedding)[0][0]

    # Check correctness (if similarity > 75%)
    if similarity > 0.75:
        session_data["correct_answers"] += 1

    # Move to next question
    session_data["current_index"] += 1
    if session_data["current_index"] < session_data["total_questions"]:
        next_question = questions[session_data["current_index"]]["Question"]
        return jsonify({"next_question": next_question, "index": session_data["current_index"]})
   
    # If no more questions, calculate score
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
        recommendation = "You’ve demonstrated a high level of skill and knowledge. Keep pushing boundaries, learning new technologies, and contributing to the tech community. Your expertise can shape the future of innovation! 🚀🔥"

    # Clear session data
    del user_sessions[job_role]

    return jsonify({
        "final_score": final_score,
        "skill_level": skill_level,
        "recommendation": recommendation
    })

# ✅ Root route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the AI-Powered Skill Assessment API!"})

# ✅ Run the app
if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pandas as pd
# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity

# # Initialize Flask app
# app = Flask(__name__)
# CORS(app, supports_credentials=True) # Allows all origins

# # File Paths
# JOB_SKILLS_PATH = "./data/job_skills.csv"
# SKILL_ASSESSMENT_PATH = "./data/skill_assessment.csv"

# # Load datasets
# job_skills_data = pd.read_csv(JOB_SKILLS_PATH)
# skill_assessment_data = pd.read_csv(SKILL_ASSESSMENT_PATH)

# # ✅ Check and fix column names
# print("Job Skills Columns:", job_skills_data.columns)
# print("Skill Assessment Columns:", skill_assessment_data.columns)

# # Load Sentence Transformer model for NLP-based similarity evaluation
# sentence_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# # Store user session data
# user_sessions = {}

# # ✅ Start assessment and return first question
# @app.route('/start_assessment', methods=['POST'])
# def start_assessment():
#     job_role = request.json.get('job_role', '').strip().lower()
   
#     # Fix column name dynamically
#     column_name = "job_role" if "job_role" in skill_assessment_data.columns else "Job Role"
   
#     print(f"Fetching questions for job role: {job_role}")  # ✅ Debugging

#     # Fetch relevant questions
#     questions_df = skill_assessment_data[skill_assessment_data[column_name].str.lower() == job_role]
   
#     if questions_df.empty:
#         return jsonify({"response": f"No assessment questions found for job role '{job_role}'."}), 404

#     questions = questions_df['Question'].tolist()
#     answers = questions_df['Answer'].tolist()

#     # Initialize user session
#     user_sessions[job_role] = {
#         "questions": questions,
#         "answers": answers,
#         "current_index": 0,
#         "score": 0
#     }

#     # Return the first question
#     return jsonify({"question": questions[0], "index": 0})
# @app.route('/get_questions', methods=['POST', 'OPTIONS'])
# def get_questions():
#     if request.method == "OPTIONS":
#         return jsonify({"message": "CORS preflight successful"}), 200  # ✅ Handles CORS preflight

#     job_role = request.json.get('job_role', '').strip().lower()

#     # Fix column name dynamically
#     column_name = "job_role" if "job_role" in skill_assessment_data.columns else "Job Role"
   
#     print(f"Fetching questions for job role: {job_role}")  # ✅ Debugging

#     # Fetch relevant questions
#     questions_df = skill_assessment_data[skill_assessment_data[column_name].str.lower() == job_role]

#     if questions_df.empty:
#         return jsonify({"response": f"No assessment questions found for job role '{job_role}'."}), 404

#     questions = questions_df['Question'].tolist()
#     return jsonify({"questions": questions})

# # ✅ Submit answer and get the next question
# @app.route('/submit_answer', methods=['POST'])
# def submit_answer():
#     user_data = request.json
#     job_role = user_data.get('job_role', '').strip().lower()
#     user_answer = user_data.get('answer', '').strip().lower()

#     print(f"Received job role: {job_role}")  # ✅ Debugging
#     print(f"Received answer: {user_answer}")  # ✅ Debugging

#     # Check if session exists
#     if job_role not in user_sessions:
#         return jsonify({"response": "No active session. Please restart assessment."}), 400

#     session = user_sessions[job_role]
   
#     # Get the current question and correct answer
#     current_index = session["current_index"]
#     correct_answer = session["answers"][current_index].strip().lower()

#     # NLP-based similarity check
#     user_embedding = sentence_model.encode([user_answer])
#     correct_embedding = sentence_model.encode([correct_answer])
#     similarity = cosine_similarity(user_embedding, correct_embedding)[0][0]

#     print(f"Question: {session['questions'][current_index]}")  # ✅ Debugging
#     print(f"User Answer: {user_answer}")  # ✅ Debugging
#     print(f"Correct Answer: {correct_answer}")  # ✅ Debugging
#     print(f"Similarity Score: {similarity}")  # ✅ Debugging

#     # Check if the answer is correct (Threshold: 0.75)
#     is_correct = similarity > 0.75
#     if is_correct:
#         session["score"] += 1

#     # Move to the next question
#     session["current_index"] += 1

#     # If there are more questions, return the next one
#     if session["current_index"] < len(session["questions"]):
#         next_question = session["questions"][session["current_index"]]
#         return jsonify({
#             "is_correct": is_correct,
#             "next_question": next_question,
#             "index": session["current_index"]
#         })

#     # If all questions are done, return final score
#     total_questions = len(session["questions"])
#     percentage = (session["score"] / total_questions) * 100 if total_questions > 0 else 0

#     # Determine skill level and recommendations
#     if percentage < 30:
#         skill_level = "Beginner"
#         recommendation = "Practice basic concepts and revisit foundational skills."
#     elif 30 <= percentage < 50:
#         skill_level = "Intermediate"
#         recommendation = "Work on projects and improve problem-solving skills."
#     elif 50 <= percentage < 80:
#         skill_level = "Advanced Intermediate"
#         recommendation = "Learn advanced topics and contribute to open-source projects."
#     else:
#         skill_level = "Expert"
#         recommendation = "Consider specializing in a niche or mentoring others."

#     print(f"Final Score: {percentage}")  # ✅ Debugging
#     print(f"Skill Level: {skill_level}")  # ✅ Debugging
#     print(f"Recommendation: {recommendation}")  # ✅ Debugging

#     # Clear session
#     del user_sessions[job_role]

#     return jsonify({
#         "is_correct": is_correct,
#         "final_score": percentage,
#         "skill_level": skill_level,
#         "recommendation": recommendation
#     })

# # ✅ Ensure all responses have the correct CORS headers
# @app.after_request
# def add_cors_headers(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
#     response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
#     return response

# # ✅ Enable preflight OPTIONS requests
# @app.route('/<path:path>', methods=['OPTIONS'])
# def options_handler(path):
#     return jsonify({"message": "CORS preflight handled"}), 200

# # ✅ Root route
# @app.route('/')
# def index():
#     return jsonify({"message": "Welcome to the AI-Powered Skill Assessment API!"})

# # ✅ Run the app
# if __name__ == '__main__':
#     app.run(debug=True)