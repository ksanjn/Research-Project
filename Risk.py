import pandas as pd

# Load your CSV data
df = pd.read_csv('custom_software_engineering_tasks.csv')

# Define a function to categorize automation risk based on the feature values
def categorize_automation_risk(row):
    # Rules for categorizing automation risk
    if row['complexity'] == 'Low' and row['human_interaction'] in ['None', 'Low']:
        return 'High Risk'
    elif row['complexity'] == 'High' and row['task_type'] == 'Creative' and row['human_interaction'] == 'High':
        return 'Low Risk'
    elif row['time_taken'] in ['Full-day', 'Half-day'] or row['frequency'] in ['Monthly', 'Occasionally']:
        return 'Medium Risk'
    else:
        return 'Medium Risk'

# Apply the risk categorization function to each row
df['risk'] = df.apply(categorize_automation_risk, axis=1)

# Save the updated DataFrame to a new CSV file
df.to_csv('updated_automation_risk_1.csv', index=False)

# Display a sample of the updated dataframe
print(df.head())
