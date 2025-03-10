from flask import Blueprint, request, jsonify
import pandas as pd
import random

quiz_bp = Blueprint('quiz_bp', __name__)

# Load skill assessment dataset
DATA_PATH = "../data/skill_assessment.csv"

# Load dataset into memory (ensure it's preloaded at startup)
try:
    df = pd.read_csv(DATA_PATH)
    df.dropna(inplace=True)  # Remove missing values if any
except Exception as e:
    print("Error loading dataset:", e)
    df = None

@quiz_bp.route('/get_quiz', methods=['POST'])
def get_quiz():
    if df is None:
        return jsonify({"error": "Dataset not loaded"}), 500

    data = request.json
    skill = data.get("skill", "").lower()

    if not skill:
        return jsonify({"error": "Skill not provided"}), 400

    # Filter questions for the selected skill
    skill_questions = df[df['Skill'].str.lower() == skill]

    if skill_questions.empty:
        return jsonify({"error": f"No questions found for skill: {skill}"}), 404

    # Select a few random questions (adjust number if needed)
    questions = skill_questions.sample(min(3, len(skill_questions))).to_dict(orient="records")

    return jsonify({"questions": questions})

