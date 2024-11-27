from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Load the trained model and vectorizer
model = joblib.load('./models/job_model.pkl')
vectorizer = joblib.load('./models/vectorizer.pkl')

# Skills data for job roles
skills_data = {
    "Data Scientist":["Python, SQL, Machine Learning"],
    "Software Engineer":["JavaScript, React, Node.js"],
    "Digital Marketer":["SEO, Content Creation, Social Media"]
}

@app.route('/real_time_assesment', methods=["POST"])
def real_time_assesment():
    data = request.json
    user_skills = data.get("skills", "").split(", ")
    job_role = data.get("job_role", "")

    if not user_skills or not job_role:
        return jsonify({"error": f"job role '{job_role}' not found!"}), 404
    
    if job_role not in skills_data:
        return jsonify({"error": f"job role '{job_role}' not found!"}), 404
    
    # Get required skills
    required_skills = set(skills_data[job_role])
    user_skills_set =set(user_skills) 

    #calculate match percentage
    matched_skills = user_skills_set & required_skills
    match_percentage = (len(matched_skills) / len(required_skills)) * 100

    # Generated recommendation
    if match_percentage < 20:
        recommendation = "You need to improve your foundational skills. start with basic courses"
    elif match_percentage < 50:
        recommendation = "Your skills are average. Focus on improving these key areas"
    else:
        recommendation = "Great job! Enchance your skills with advanvec topics"

    return jsonify({
        "job_role": job_role,
        "match_percentage": match_percentage,
        "recommendation": recommendation,
        "missing_skills": list(required_skills - user_skills_set)
    })

if __name__ == '__main__':
    app.run(debug=True)