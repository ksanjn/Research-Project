from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load models and preprocessing artifacts
MODEL_PATH = "models/chatbot_model.h5"
TOKENIZER_PATH = "models/tokenizer.pkl"
LABEL_ENCODER_PATH = "models/label_encoder.pkl"
DATA_PATH = "data/job_roles.csv"

# Load the trained model, tokenizer, label encoder, and dataset
model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, 'rb') as tok_file:
    tokenizer = pickle.load(tok_file)
with open(LABEL_ENCODER_PATH, 'rb') as le_file:
    label_encoder = pickle.load(le_file)

job_data = pd.read_csv(DATA_PATH)

# Preprocess user input
def preprocess_input(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')
    return padded_sequence

# Fetch questions for a job role
@app.route('/get_questions', methods=['POST'])
def get_questions():
    job_role = request.json.get('job_role', '').strip()

    # Filter dataset for the requested job role
    job_row = job_data[job_data['job_title'].str.lower() == job_role.lower()]
    if job_row.empty:
        return jsonify({"response": f"No data found for job role '{job_role}'."}), 404

    questions = job_row.iloc[0]['assessment_questions'].split(';')
    return jsonify({"questions": questions})

# Evaluate answers submitted by the user
@app.route('/evaluate_answers', methods=['POST'])
def evaluate_answers():
    user_data = request.json
    job_role = user_data.get('job_role', '').strip()
    user_answers = user_data.get('answers', {})

    # Get correct answers for the job role
    job_row = job_data[job_data['job_title'].str.lower() == job_role.lower()]
    if job_row.empty:
        return jsonify({"response": f"No data found for job role '{job_role}'."}), 404

    correct_answers = job_row.iloc[0]['answers'].split(';')
    correct_answers_dict = dict(zip(
        [f"Q{i+1}" for i in range(len(correct_answers))],
        correct_answers
    ))

    # Evaluate user answers
    total_questions = len(correct_answers_dict)
    score = 0
    for question, user_answer in user_answers.items():
        correct_answer = correct_answers_dict.get(question, "").strip().lower()
        if user_answer.strip().lower() == correct_answer:
            score += 1

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
