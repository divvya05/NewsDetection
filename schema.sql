-- Drop existing tables if they exist to avoid conflicts during initialization
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS detection_history;

-- Create the users table to store user credentials
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- Create the detection_history table to store news detection results
CREATE TABLE detection_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    news_text TEXT,
    is_fake BOOLEAN,
    reason TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


