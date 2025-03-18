import sqlite3

def init_db():
    # Connect to the SQLite database (it will be created if it doesn't exist)
    connection = sqlite3.connect('database/db.sqlite3')  # Adjust the path if necessary

    # Open the schema.sql file and execute its commands
    with open('schema.sql') as f:
        connection.executescript(f.read())  # Execute all SQL commands in schema.sql

    # Insert initial user data
    insert_user(connection, 'admin', 'password123')  # Insert user with username 'admin' and password 'password123'

    connection.close()  # Close the database connection
    print("Database initialized successfully.")

def insert_user(conn, username, password):
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()

if __name__ == '__main__':
    init_db()  # Call the init_db function to run the script
