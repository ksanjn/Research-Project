import pandas as pd

#Load the dataset
job_roles_data = pd.read_csv('../data/job_roles.csv')

# Convert to dictionary for quick lookup
job_dict = {
    row['job_title']: {
        "required_skills": row['required_skills'].split(', '),
        "assessment_questions": row['assessment_questions'].split(';'),
        "answers": dict(zip(
            [f"Q{i+1}" for i in range(len(row['assessment_questions'].split(';')))],
            row['answers'].split(';')
        ))
    }
    for _, row in job_roles_data.iterrows()
}

#Display the first few rows of the dataset to check(single file)
print("Job data loaded successfully!")













