import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Paths
DATA_PATH = "../data/job_roles.csv"
MODEL_SAVE_PATH = "../models/chatbot_model.h5"
TOKENIZER_SAVE_PATH = "../models/tokenizer.pkl"
LABEL_ENCODER_PATH = "../models/label_encoder.pkl"

# Load Dataset
def load_data(file_path):
    df = pd.read_csv(file_path)
    return df

# Preprocess Data
def preprocess_data(df):
    df['text'] = df['job_title'] + " " + df['required_skills'] + " " + df['assessment_questions']
    tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
    tokenizer.fit_on_texts(df['text'])
    sequences = tokenizer.texts_to_sequences(df['text'])
    padded_sequences = pad_sequences(sequences, maxlen=100, padding='post')

    label_encoder = LabelEncoder()
    labels = label_encoder.fit_transform(df['job_title'])  # Ensure labels start from 0
    num_classes = len(label_encoder.classes_)  # Number of unique classes

    return padded_sequences, labels, tokenizer, label_encoder, num_classes

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
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

# Train Model
def train_model(data, labels, tokenizer, label_encoder, num_classes):
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)
    model = build_model(input_dim=len(tokenizer.word_index) + 1, num_classes=num_classes)
    model.fit(X_train, y_train, epochs=10, validation_data=(X_test, y_test), batch_size=32)

    # Save model and artifacts
    model.save(MODEL_SAVE_PATH)
    with open(TOKENIZER_SAVE_PATH, 'wb') as tok_file:
        pickle.dump(tokenizer, tok_file)
    with open(LABEL_ENCODER_PATH, 'wb') as le_file:
        pickle.dump(label_encoder, le_file)

    print("Model, tokenizer, and label encoder saved successfully!")

# Main Script
if __name__ == "__main__":
    df = load_data(DATA_PATH)
    data, labels, tokenizer, label_encoder, num_classes = preprocess_data(df)
    train_model(data, labels, tokenizer, label_encoder, num_classes)
