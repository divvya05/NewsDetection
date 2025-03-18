from flask import Flask, render_template, request, redirect, url_for, flash, session
import pandas as pd
import sqlite3
import os  # Import os module for generating random secret key

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a random secret key

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
        conn.close()

        if user:
            session['user_id'] = user['id']  # Save user ID in session
            session['username'] = user['username']  # Save username in session
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))  # Redirect to index.html after successful login
        else:
            flash('Invalid credentials. Please try again.', 'danger')

    return render_template('login.html')

# Index route (main dashboard)
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

    return render_template('stats.html')  # Render stats.html


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

# Fake News Detection route
@app.route('/detect', methods=['POST'])
def detect():
    news_text = request.form['news_text']
    
    # Here you would typically call your machine learning model to classify the news.
    # For demonstration purposes, let's assume we just return a dummy result.
    
    is_fake = False  # Replace this with your actual prediction logic
    result = "This news is classified as " + ("fake" if is_fake else "true") + "."
    reason = "This classification is based on the text patterns analyzed by the model."

    return render_template('index.html', result=result, reason=reason)

if __name__ == '__main__':
    app.run(debug=True)
