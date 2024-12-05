![image](https://github.com/user-attachments/assets/e70dbd5e-20c1-4b43-864b-9a0a4df815aa)
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

## AI-Assistant diagram
![image](https://github.com/user-attachments/assets/d0d59aa3-da62-4da8-98b7-43d6732e08c3)

## Description
A real-time chatbot that evaluates skills for specific job roles, provides assessments, scores user answers, and recommends ways to improve.

## Features
- Real-time chatbot interaction.
- Assessment question generation.
- Answer evaluation and scoring.
- Skill improvement recommendations.

## Models used
- Natural Language Processing (NLP) and LSTM

## Algorithm used
- Multinomial Naive Bayes
- Cosine Similarity
- Jaccard Similarity
- Logistic Regression

## Technologies Used
- Frontend: React.js, Tailwind CSS.
- Backend: Flask, TensorFlow, Pandas.

## The way of create AI-Assistent
- Processing and structuring the job role data
```
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
```

- Training a ML model for Job role to using NLP and LSTM
```
# Preprocess Data
def preprocess_data(df):
    df['text'] = df['job_title'] + " " + df['required_skills'] + " " + df['assessment_questions'] # Combine the text columns into single text column
    tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>") # A tokenizer convert the text into numerical sequences
    tokenizer.fit_on_texts(df['text'])
    sequences = tokenizer.texts_to_sequences(df['text'])
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post')

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(df['job_title'])  # Ensure labels start from 0
    num_classes = len(label_encoder.classes_)  # Number of unique classes

    return padded_sequences, labels, tokenizer, label_encoder, num_classes
```
```
This model process text input and predict job role.
# Build Model
def build_model(input_dim, num_classes):
    model = Sequential([
        Embedding(input_dim=input_dim, output_dim=128, input_length=100),
        LSTM(128, return_sequences=True),
        Dropout(0.2),
        LSTM(64),
        Dense(32, activation='relu'),
        Dense(num_classes, activation='softmax')  # Softmax for multi-class classification
    ])

# The metrics=[‘accuracy’] specifies that the model should calculate the accuracy during the training and validation
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model
```
```
Train the model using following steps and finally save the trained model 
# Train Model
def train_model(data, labels, tokenizer, label_encoder, num_classes):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    model = build_model(input_dim=len(tokenizer.word_index) + 1, num_classes=num_classes)
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=32)

    # Save model and artifacts
    model.save(MODEL_SAVE_PATH) # “chatbot_model.h5”, tokenizer and label encoder for future use.
    with open(TOKENIZER_SAVE_PATH, 'wb') as tok_file:
        pickle.dump(tokenizer, tok_file)
    with open(LABEL_ENCODER_PATH, 'wb') as le_file:
        pickle.dump(label_encoder, le_file)

    print("Model, tokenizer, and label encoder saved successfully!")

    predictions = model.predict(X_test)
    print("Predictions:", predictions[:5])
    print("True Labels:", y_test[:5])
```
- Building a Flask-based job role with ML integration
```
# Preprocess user input
def preprocess_input(user_input):
    sequence = tokenizer.texts_to_sequences([user_input])
    padded_sequence = pad_sequences(sequence, maxlen=100, padding='post')
    return padded_sequence
```
```
# Fetch questions for a job role
@app.route('/get_questions', methods=['POST'])
def get_questions():
    job_role = request.json.get('job_role', '').strip()  # User input job role

    # Filter dataset for the requested job role
    job_row = job_roles_data[job_roles_data['job_title'].str.lower() == job_role.lower()]
    if job_row.empty:
        return jsonify({"response": f"No data found for job role '{job_role}'."}), 404

    questions = job_row.iloc[0]['assessment_questions'].split(';')
    return jsonify({"questions": questions})
```
```
# Evaluate answers submitted by the user
@app.route('/evaluate_answers', methods=['POST'])
def evaluate_answers():
    user_data = request.json
    job_role = user_data.get('job_role', '').strip()
    user_answers = user_data.get('answers', {})  # User-submitted answers

    # Debug: Log user inputs
    print(f"Job Role: {job_role}")
    print(f"User Answers: {user_answers}")
```
Use fuzz.ratio to compare answers with a similarity threshold of 90%
```
 if fuzz.ratio(user_answer_normalized, correct_answer) > 90:  # Threshold is 90%
            score += 1

## AI-Assitant sample output
- Enter the job role for the chatbot 
![image](https://github.com/user-attachments/assets/448901df-a2ec-4363-9151-a9984ed4b2b7)

- Provide assessment(MCQs, coding questions, structure question) based on job roles
![image](https://github.com/user-attachments/assets/9edc82f5-5454-4954-b0a0-b7f1f1aef728)

- Evaluate user answers, calculate scores, and categorize skill levels ( Low, Intermediate, High).
![image](https://github.com/user-attachments/assets/6b1df5c1-294e-46c3-bfcc-97268bf9c97d)

# COMPONENT#4 -  Recommending Tailor-Made Learning Pathways

## Overview

This component focuses on recommending personalized learning pathways to help software engineers achieve new skillsets tailored to their preferences. Staying updated with new skills is vital in the software engineering domain, and this module aims to fill skill gaps by creating targeted pathways that align with individual needs.

### Key Highlights
- Emphasis on user-specific preferences and career goals.
- Addressing the gap in current AI tools that overlook personalization in learning pathways.
- Recommends skills and courses based on user availability, budget, and existing knowledge.

---

## **Architecture Diagram**


---

## **Technologies**
- **Programming Language**: Python
- **Frontend**: React, CSS, JS
- **Database**: MySQL
- **Platforms**: Google Colab

---

## **Techniques and Algorithms**
- **Supervised Learning Techniques**:
  - K-Nearest Neighbors (KNN)
  - Linear Regression
- **Natural Language Processing (NLP)** for content alignment
- Filtering and Clustering

---

## **Completed Work**
1. Problem definition and research focus.
2. Data collection and preprocessing.
3. Integration of user preferences such as:
   - Budget
   - Time slots
   - Learning mode (online/on-premises)
4. Training and testing the KNN & Linear Regression models.
5. Basic analysis and insights generation.

---

## **Future Work**
1. Advanced model refinements.
2. Creating APIs and integrating them with the web application.

