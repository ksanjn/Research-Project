
# 24-25J-113 Research-Project

As an overview, the aim of this research project is to try and identify the various software engineering jobs that are at risk of getting automated by AI and suggesting better jobs that are at less risk of getting automated while providing necessary help to bridge the knowledge gap between the jobs.

The main idea is broken down to four specific components as,

 - Identifying the current software engineering tasks that are replaced by AI and tasks that could be replaced in future by AI.
 - Identifying alternative software engineering jobs with tasks similar to the user's current tasks that are less likely to be automated by AI.
 - Assessing the current skillset of the user and identifying the skills that the user is lacking that is needed for the new suggested role.
 - Identifying the user preferences and recommending the best suited pathways to achieving the new skills.

## Architecture Diagram

![Proposed Solution Architecture](https://github.com/user-attachments/assets/af092fbe-7714-4f96-b98a-9822968c1b2f)

## Dependencies

- Python / ML Libararies
- React
- NodeJS
- MongoDB
- Google Cloud Platform

# COMPONENT#1 - Identifying Job Roles At Risk Of Automation

## Architecture Diagram

<img width="648" alt="my-arch" src="https://github.com/user-attachments/assets/02cbfb12-db98-4c2c-9b7d-5403d43c1f63">

####
Achieved by identifying the specific individual tasks under particular job roles and evaluating the individual task automation probability.

Real-world software engineer data will be used for the prediction.

Automation probability is calculated using the following considerations:

- Has the task already been automated by AI?
- If not does it have a chance of being automated by AI in the future?

Two separate Logistic Regression ML models will be used for the predictions.

### Sample input for identifying already automated tasks
```
new_task = ["integration tests"]
new_task_vectorized = vectorizer.transform(new_task)
prediction = model.predict(new_task_vectorized)
print(f"Prediction: {'Automated' if prediction[0] == 1 else 'Not Automated'}")
```

### Sample Output
```
Prediction: Automated
```

# COMPONENT#2 - Identify alternative software engineering jobs with tasks similar to the user's current tasks that are less likely to be automated by AI using a ML approach.

## Description
Develop an ML model to recommend alternative job roles less likely to be automated, based on a user's current role and tasks.

## Architecture Diagram

![image](https://github.com/user-attachments/assets/b63b5b5b-cae5-4904-9eb0-31b6a86fd367)

Automation risk was calculated by considering below data:
- complexity
- task_type
- creativity
- human_interaction
- time_taken
- frequency


## Algorithm used
- Random Forest

## Techniques used
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Cosine Similarity


### Sample input for identifying similar job roles:
```
job_description = input("Enter a task or description: ")
recommendations = get_recommendations_from_input(job_description)
print("Recommendations:\n", recommendations)
```
```
Enter a task or description: Conduct user research
```
### Sample output:
```
Recommendations:
                job_role Automation_Risk  \
579     DevOps Engineer     Medium Risk   
126   Software Engineer     Medium Risk   
573  Frontend Developer     Medium Risk   
257     DevOps Engineer        Low Risk   
556         QA Engineer        Low Risk   

                                      Mapped_Skills  
579                        [other, teamwork, other]  
126                        [other, teamwork, other]  
573  [technical skills, teamwork, technical skills]  
257                 [other, other, teamwork, other]  
556                        [other, teamwork, other]  
```

# COMPONENT#3 - Job Role Skill Assessment Chatbot

## Description
A real-time chatbot that evaluates skills for specific job roles, provides assessments, scores user answers, and recommends ways to improve.

## Features
- Real-time chatbot interaction.
- Assessment question generation.
- Answer evaluation and scoring.
- Skill improvement recommendations.

## Models used
- Multinomial Naive Bayes
- Logistic Regression

## Algorithm used
- TF-IDF (Term Frequency-Inverse Document Frequency)
- Cosine Similarity
- Jaccard Similarity 

## Technologies Used
- Frontend: React.js, Tailwind CSS.
- Backend: Flask, TensorFlow, Pandas.

## AI-Assistant diagram
![image](https://github.com/user-attachments/assets/d0d59aa3-da62-4da8-98b7-43d6732e08c3)

