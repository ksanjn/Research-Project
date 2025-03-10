import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sentence_transformers import SentenceTransformer
from imblearn.over_sampling import SMOTE
from collections import Counter
import pickle

# Paths
DATA_PATH = "../data/skill_assessment.csv"
MODEL_SAVE_PATH = "../models/skill_classifier.pkl"
LABEL_ENCODER_PATH = "../models/label_encoder.pkl"

# Load Dataset
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        df.dropna(subset=['Question', 'Answer'], inplace=True)  # Remove rows with missing values
        df.drop_duplicates(inplace=True)  # Remove duplicate questions
        return df
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None

# Preprocess Data
def preprocess_data(df, model):
    if 'Question' not in df.columns or 'Answer' not in df.columns:
        raise ValueError("Dataset missing required columns: 'Question' or 'Answer'")

    # Batch encoding for efficiency
    question_embeddings = model.encode(df['Question'].tolist(), convert_to_numpy=True)

    # Encode skill levels
    label_encoder = LabelEncoder()
    df['skill_level'] = label_encoder.fit_transform(df['Answer'])  

    return question_embeddings, df['skill_level'].values, label_encoder

# Train Model
def train_model(features, labels, label_encoder):
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    # Check class distribution before applying SMOTE
    class_counts = Counter(y_train)
    print("Class distribution before SMOTE:", class_counts)

    # Apply SMOTE only if all classes have at least 2 samples
    if min(class_counts.values()) > 1:
        smote = SMOTE(random_state=42, k_neighbors=min(5, min(class_counts.values()) - 1))
        X_train, y_train = smote.fit_resample(X_train, y_train)
        print("✅ Applied SMOTE")
    else:
        print("⚠️ Skipping SMOTE due to insufficient samples in some classes")

    # Train the RandomForest model
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    # Model evaluation
    y_pred = model.predict(X_test)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"Recall: {recall_score(y_test, y_pred, average='weighted'):.4f}")
    print(f"F1 Score: {f1_score(y_test, y_pred, average='weighted'):.4f}")

    # Save model and label encoder
    with open(MODEL_SAVE_PATH, 'wb') as model_file:
        pickle.dump(model, model_file)
    with open(LABEL_ENCODER_PATH, 'wb') as le_file:
        pickle.dump(label_encoder, le_file)

    print("✅ Model and label encoder saved successfully!")

# Main Script
if __name__ == "__main__":
    print("🚀 Loading dataset...")
    df = load_data(DATA_PATH)

    if df is not None:
        print("✅ Dataset loaded successfully!")
       
        print("🚀 Loading Sentence Transformer model...")
        model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
       
        print("🚀 Preprocessing data...")
        features, labels, label_encoder = preprocess_data(df, model)
       
        print("🚀 Training model...")
        train_model(features, labels, label_encoder)
    else:
        print("❌ Failed to load dataset. Check the CSV file.")