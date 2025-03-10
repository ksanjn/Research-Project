def calculate_skill_gap(user_skills, required_skills):
    missing_skills = [skill for skill in required_skills if skill not in user_skills]
    return missing_skills
