from flask import Flask, render_template, request
import pandas as pd
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

# Load the trained model and vectorizer from the `model/` folder
with open("model/model.pkl", "rb") as f:
    rf_model, vectorizer, categorical_encoded = pickle.load(f)

# Load the dataset from the `model/` folder
dataset = pd.read_csv("model/processed_dataset.csv")

app = Flask(__name__)

# Home page with input form
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Get user input
    job_description = request.form['job_description']

    # Preprocess the input job description
    processed_input = " ".join(re.split(r'[.\n;]', job_description))
    input_text_vectorized = vectorizer.transform([processed_input]).toarray()

    # Recompute training features (X)
    text_features = vectorizer.transform(dataset['Job_Description'].fillna('')).toarray()
    dummy_categorical = np.zeros((dataset.shape[0], categorical_encoded.shape[1]))  # Dummy categorical features for training data
    X = np.hstack([dummy_categorical, text_features])  # Recombine categorical and text features

    # Create input features for the new job description
    dummy_input_categorical = np.zeros((1, categorical_encoded.shape[1]))
    input_features = np.hstack([dummy_input_categorical, input_text_vectorized])

    # Compute similarity
    similarity_scores = cosine_similarity(input_features, X)
    similar_indices = similarity_scores.argsort()[0, -5:][::-1]  # Get top 5 most similar jobs
    recommendations = dataset.iloc[similar_indices]

    # Pass recommendations to the HTML template
    return render_template('recommendations.html', recommendations=recommendations.to_dict(orient='records'))


if __name__ == "__main__":
    app.run(debug=True)
