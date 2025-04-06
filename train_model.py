import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

# Load the dataset
true_data = pd.read_csv('true.csv')
fake_data = pd.read_csv('fake.csv')

# Combine the datasets
data = pd.concat([true_data, fake_data], ignore_index=True)

# Prepare features and labels
X = data['text']
y = [1] * len(true_data) + [0] * len(fake_data)  # 1 for true, 0 for fake

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Vectorization using TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
X_train_vectorized = vectorizer.fit_transform(X_train)
X_test_vectorized = vectorizer.transform(X_test)

# Train the Logistic Regression model
model = LogisticRegression(max_iter=20000)
model.fit(X_train_vectorized, y_train)

# Make predictions
y_pred = model.predict(X_test_vectorized)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Generate classification report
report = classification_report(y_test, y_pred)
print(report)

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)

# Plotting the Confusion Matrix
plt.figure(figsize=(10, 6))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=['Fake', 'True'], yticklabels=['Fake', 'True'])
plt.ylabel('Actual')
plt.xlabel('Predicted')
plt.title('Confusion Matrix')
plt.savefig('static/confusion_matrix.png')  # Save confusion matrix image

# Plotting Accuracy Graph
plt.figure(figsize=(10, 6))
plt.plot([1, 2], [0.90, accuracy], marker='o', label='Accuracy')
plt.title('Model Accuracy')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.xticks([1, 2], ['Initial', 'Final'])
plt.legend()
plt.grid()
plt.savefig('static/model_accuracy.png')  # Save accuracy plot

# Save the model and vectorizer for later use in app.py
with open('models/fake_news_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('models/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)

print("Model training complete and saved.")
