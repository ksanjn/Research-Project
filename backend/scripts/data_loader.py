import pandas as pd

# File Paths
job_skills_path = "../data/job_skills.csv"
skill_assessment_path = "../data/skill_assessment.csv"
recommendation_path = "../data/recommendation.csv"

# Load job skills dataset
try:
    job_skills_df = pd.read_csv(job_skills_path)
    job_skills_df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)  # Drop unnamed index column if present
    job_skills_df.drop_duplicates(inplace=True)
except Exception as e:
    print("Error loading job skills dataset:", e)
    job_skills_df = None

# Load skill assessment dataset
try:
    skill_assessment_df = pd.read_csv(skill_assessment_path)
except Exception as e:
    print("Error loading skill assessment dataset:", e)
    skill_assessment_df = None

# Load recommendation dataset
try:
    recommendation_df = pd.read_csv(recommendation_path)
except Exception as e:
    print("Error loading recommendation dataset:", e)
    recommendation_df = None

# Handle missing values in skill assessment dataset
if skill_assessment_df is not None:
    for column in skill_assessment_df.columns:
        if skill_assessment_df[column].dtype == 'object':  # Categorical data
            skill_assessment_df[column] = skill_assessment_df[column].fillna("Unknown")
        else:  # Numerical data
            skill_assessment_df[column] = skill_assessment_df[column].fillna(skill_assessment_df[column].median())

# Convert job skills data to dictionary for quick lookup
# Skill Gap Analysis with Recommendation
def analyze_skill_gap(user_skills, job_role, score):
    """
    Compares user's existing skills with required skills for a job role
    and provides personalized recommendations based on score.
    """
    if job_skills_df is not None:
        job_role_row = job_skills_df[job_skills_df['job_role'].str.lower() == job_role.lower()]

        if not job_role_row.empty:
            required_skills = set(job_role_row.iloc[0]['skill'].split(',')) if isinstance(job_role_row.iloc[0]['skill'], str) else set()
            user_skills_set = set(user_skills)

            missing_skills = required_skills - user_skills_set
            acquired_skills = required_skills & user_skills_set

            # Get recommendation based on score
            recommendation = get_recommendation(score)

            return {
                "required_skills": list(required_skills),
                "missing_skills": list(missing_skills),
                "acquired_skills": list(acquired_skills),
                "recommendation": recommendation
            }
        else:
            return {"error": f"No skills found for job role '{job_role}'"}
    return {"error": "Job skills dataset is not loaded"}


# Get Real-Time Recommendation Based on Score
def get_recommendation(score):
    """
    Retrieve the recommendation message for a given score from recommendation.csv
    """
    if recommendation_df is not None:
        # Find the closest score recommendation
        closest_row = recommendation_df.iloc[(recommendation_df['score'] - score).abs().argsort()[:1]]
        return closest_row['recommendation'].values[0] if not closest_row.empty else "No recommendation found"
    return "Recommendation dataset not loaded."


print("\nDatasets loaded and processed successfully!")
