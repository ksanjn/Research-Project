from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from fuzzywuzzy import fuzz

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load models and preprocessing artifacts
MODEL_PATH = "./models/chatbot_model.h5"
TOKENIZER_PATH = "./models/tokenizer.pkl"
LABEL_ENCODER_PATH = "./models/label_encoder.pkl"
DATA_PATH = "./data/job_roles.csv"

# Load the trained model, tokenizer, label encoder, and dataset
model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as tok_file:
    tokenizer = pickle.load(tok_file)
with open(LABEL_ENCODER_PATH, 'rb') as le_file:
    label_encoder = pickle.load(le_file)

# Load dataset into a variable with a meaningful name
job_roles_data = pd.read_csv(DATA_PATH)

# Preprocess user input
def preprocess_input(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')
    return padded_sequence

# Fetch questions for a job role
@app.route('/get_questions', methods=['POST'])
def get_questions():
    job_role = request.json.get('job_role', '').strip()  # User input job role

    # Filter dataset for the requested job role
    job_row = job_roles_data[job_roles_data['job_title'].str.lower() == job_role.lower()]
    if job_row.empty:
        return jsonify({"response": f"No data found for job role '{job_role}'."}), 404

    questions = job_row.iloc[0]['assessment_questions'].split(';')
    return jsonify({"questions": questions})

# Evaluate answers submitted by the user
@app.route('/evaluate_answers', methods=['POST'])
def evaluate_answers():
    user_data = request.json
    job_role = user_data.get('job_role', '').strip()
    user_answers = user_data.get('answers', {})  # User-submitted answers

    # Debug: Log user inputs
    print(f"Job Role: {job_role}")
    print(f"User Answers: {user_answers}")

    # Get correct answers for the job role
    job_row = job_roles_data[job_roles_data['job_title'].str.lower() == job_role.lower()]
    if job_row.empty:
        return jsonify({"response": f"No data found for job role '{job_role}'."}), 404

    # Extract correct answers and split by ';'
    correct_answers = job_row.iloc[0]['answers'].split(';')
    correct_answers_dict = dict(zip(
        [f"Q{i+1}" for i in range(len(correct_answers))],
        correct_answers
    ))

    # Debug: Log the correct answers
    print(f"Correct Answers: {correct_answers_dict}")

    total_questions = len(correct_answers_dict)
    score = 0


    

    # Loop over user answers and compare with correct answers
    for question, user_answer in user_answers.items():
        # Normalize answers
        correct_answer = correct_answers_dict.get(question, "").strip().lower()
        user_answer_normalized = user_answer.strip().lower()

        # Debug: Log comparison of each answer
        print(f"Question: {question}")
        print(f"User Answer: {user_answer_normalized}")
        print(f"Correct Answer: {correct_answer}")

        # Compare answers with fuzzy matching
        #if correct_answer == user_answer_normalized:  # Exact match
            #score += 1
        if fuzz.ratio(user_answer_normalized, correct_answer) > 90:  # Threshold is 90%
            score += 1

    # Debug: Log final score
    print(f"Total Correct Answers: {score} out of {total_questions}")

    # Calculate percentage
    percentage = (score / total_questions) * 100

    # Determine skill level and recommendations
    if percentage < 30:
        skill_level = "Low"
        recommendation = "Practice basic coding concepts and revisit foundational skills."
    elif 30 <= percentage < 50:
        skill_level = "Intermediate"
        recommendation = "Focus on intermediate projects and work on problem-solving."
    elif 50 <= percentage < 80:
        skill_level = "Advanced Intermediate"
        recommendation = "Learn advanced topics and contribute to open-source projects."
    else:
        skill_level = "High"
        recommendation = "Explore leadership opportunities and specialize in advanced topics."

    # Debug: Log the final output
    print(f"Percentage: {percentage}, Skill Level: {skill_level}, Recommendation: {recommendation}")

    return jsonify({
        "score": percentage,
        "skill_level": skill_level,
        "recommendation": recommendation
    })

# Predict job role based on user input
@app.route('/predict_job_role', methods=['POST'])
def predict_job_role():
    user_input = request.json.get('user_input', '').strip()
    if not user_input:
        return jsonify({"response": "No input provided."}), 400

    # Preprocess and predict
    processed_input = preprocess_input(user_input)
    prediction = model.predict(processed_input)
    predicted_label = label_encoder.inverse_transform([prediction.argmax()])[0]

    return jsonify({"predicted_job_role": predicted_label})

# Root route
@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Job Role Skill Assessment API!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
