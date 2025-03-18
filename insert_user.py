import sqlite3

def insert_user(username, password):
    conn = sqlite3.connect('database/db.sqlite3')  # Adjust the path if necessary
    conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()

# Example usage: Insert a user with username 'admin' and password 'password123'
if __name__ == '__main__':
    insert_user('admin', 'password123')
    print("User 'admin' inserted successfully.")
