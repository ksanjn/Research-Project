import pandas as pd

# Load the datasets
job_skills_path = "../data/job_skills.csv"
skill_assessment_path = "../data/skill_assessment.csv"

# Read job skills dataset
try:
    job_skills_df = pd.read_csv(job_skills_path)
    job_skills_df.drop(columns=['Unnamed: 0'], errors='ignore', inplace=True)  # Drop unnamed index column if present
    job_skills_df.drop_duplicates(inplace=True)
except Exception as e:
    print("Error loading job skills dataset:", e)
    job_skills_df = None

# Read skill assessment dataset
try:
    skill_assessment_df = pd.read_csv(skill_assessment_path)
except Exception as e:
    print("Error loading skill assessment dataset:", e)
    skill_assessment_df = None

# Handle missing values if dataset loaded successfully
if skill_assessment_df is not None:
    for column in skill_assessment_df.columns:
        if skill_assessment_df[column].dtype == 'object':  # Categorical data
            skill_assessment_df[column] = skill_assessment_df[column].fillna("Unknown")
        else:  # Numerical data
            skill_assessment_df[column] = skill_assessment_df[column].fillna(skill_assessment_df[column].median())

# Skill Gap Analysis Function
def analyze_skill_gap(user_skills, job_role):
    """ Compares user's existing skills with required skills for a job role """
    if job_skills_df is not None:
        job_role_row = job_skills_df[job_skills_df['job_role'].str.lower() == job_role.lower()]
       
        if not job_role_row.empty:
            required_skills = set(job_role_row.iloc[0]['skill'].split(','))
            user_skills_set = set(user_skills)

            missing_skills = required_skills - user_skills_set
            acquired_skills = required_skills & user_skills_set

            return {
                "required_skills": list(required_skills),
                "missing_skills": list(missing_skills),
                "acquired_skills": list(acquired_skills)
            }
        else:
            return {"error": f"No skills found for job role '{job_role}'"}
    return {"error": "Job skills dataset is not loaded"}

# Convert job skills data to dictionary for quick lookup
job_dict = {}
if job_skills_df is not None:
    job_dict = {
        row['job_role']: {
            "required_skills": row['skill'].split(',') if isinstance(row['skill'], str) else []
        }
        for _, row in job_skills_df.iterrows()
    }

# Convert skill assessment data into structured format
skill_assessments = {}
if skill_assessment_df is not None:
    for _, row in skill_assessment_df.iterrows():
        skill = row['Skill']
        if skill not in skill_assessments:
            skill_assessments[skill] = []

        # Ensure 'Options' exists, handle missing values
        options = row.get('Options', None)
        if isinstance(options, str) and ',' in options:
            options = options.split(',')
        elif options == "Unknown":
            options = None

        skill_assessments[skill].append({
            "question": row['Question'],
            "type": row['Type'],
            "options": options,
            "answer": row['Answer']
        })

print("\n✅ Datasets loaded and processed successfully!")