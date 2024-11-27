from sklearn.feature_extraction.text import TfidfVectorizer;
from sklearn.naive_bayes import MultinomialNB;
from sklearn.model_selection import train_test_split
import joblib
import pandas as pd

# Load the dataset
data = pd.read_csv("../data/job_roles.csv")

data['required_skills']=data['required_skills'].apply(lambda x:''.join(x.split(',')))

# convert skills to mumerical data
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(data['required_skills'])
y = data['job_title']

X_dense = X.toarray()

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_dense, y, test_size=0.3, random_state=42)

# Train the model
model = MultinomialNB()
model.fit(X_train,y_train)

# Test the model
accuracy = model.score(X_test,y_test)
print(f"Model Accuracy:{accuracy *100:.2f}%")

# Save the model and Vectorizer
joblib.dump(model, '../models/job_model.pkl')
joblib.dump(vectorizer, '../models/vectorizer.pkl')

print("Model and Vectorizer saved successfully")