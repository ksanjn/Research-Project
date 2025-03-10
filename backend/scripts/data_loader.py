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

# Debugging: Print column names
if job_skills_df is not None:
    print("Job Skills Columns:", job_skills_df.columns)
if skill_assessment_df is not None:
    print("Skill Assessment Columns:", skill_assessment_df.columns)

# Convert job skills data to dictionary for quick lookup
if job_skills_df is not None:
    job_dict = {
        row['job_role']: {
            "required_skills": row['skill'].split(',') if isinstance(row['skill'], str) else []
        }
        for _, row in job_skills_df.iterrows()
    }
else:
    job_dict = {}

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

# Debugging: Print sample data
if job_dict:
    print("\nSample Job Role Data:", list(job_dict.items())[:2])
if skill_assessments:
    print("\nSample Skill Assessment Data:", list(skill_assessments.items())[:2])

print("\n✅ Datasets loaded and processed successfully!")