from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import sqlite3
import pickle
import os  # Import os module for generating random secret key

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key
print("Secret key: ", app.secret_key)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('database/db.sqlite3')  # Adjust the path if necessary
    conn.row_factory = sqlite3.Row  # Allows name-based access to columns by name
    return conn

# Home route redirects to login page
@app.route('/')
def home():
    return redirect(url_for('login'))  # Redirect to login page

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'] 
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        conn.execute('SELECT * FROM users').fetchone()
        conn.close()

        if user:
            session['user_id'] = user['id']  # Save user ID in session
            session['username'] = user['username']  # Save username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to index.html after successful login
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Index route (main dashboard)+
@app.route('/index')
def index():
    if 'user_id' not in session:  # Check if user is logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('index.html', username=session['username'])  # Render index.html

# Stats route
@app.route('/stats')
def stats():
    if 'user_id' not in session:  # Check if user is logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    
    classification_report = """\
              precision    recall  f1-score   support

           0       0.99      0.98      0.99      4650
           1       0.98      0.99      0.99      4330

    accuracy                           0.99      8980
   macro avg       0.99      0.99      0.99      8980
weighted avg       0.99      0.99      0.99      8980"""

    return render_template('stats.html',accuracy = 98.80, classification_report=classification_report )  # Render stats.html


# Team route
@app.route('/team')
def team():
    if 'user_id' not in session:  # Check if user is logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    return render_template('team.html')  # Render team.html

# About route
@app.route('/about')
def about():
    if 'user_id' not in session:  # Check if user is logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    return render_template('about.html')  # Render about.html

# Logout route
@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    session.pop('username', None)  # Remove username from session
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))  # Redirect to login page after logout

# Define Load Model and Vectorizer Function
def load_model_and_vectorizer():
    try:
        with open('models/fake_news_model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return model, vectorizer
    except FileNotFoundError:
        print("Error: Model or vectorizer file not found. Please train the model first.")
        return None, None

# Fake News Detection route
@app.route('/detect', methods=['POST'])
def detect():
    if 'user_id' not in session:  # Check if user is logged in
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))

    # Take News Text Input
    news_text = request.form['news_text']

    # Load the trained model and vectorizer
    fake_news_model, vectorizer = load_model_and_vectorizer()

    if fake_news_model is None or vectorizer is None:
        flash("Model not loaded. Please train the model and restart the application.", "error")
        return render_template('index.html', username=session['username'])

    # Vectorize the input text
    news_text_vectorized = vectorizer.transform([news_text])

    # Make prediction
    prediction = fake_news_model.predict(news_text_vectorized)[0]  # Get the prediction (0 or 1)

    # Determine the result and reason based on the prediction
    is_fake = prediction == 0  # 0 means fake, 1 means true
    result = "This news is classified as " + ("fake" if is_fake else "true") + "."
    reason = "This classification is based on the text patterns analyzed by the model."

    return render_template('index.html', username=session['username'], result=result, reason=reason)


if __name__ == '__main__':
    app.run(debug=True)
