import sqlite3

def show_users():
    conn = sqlite3.connect(r"/financial_tracker/fi.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user;")
    users = cursor.fetchall()
    for user in users:
        print(user)
    conn.close()

def add_user(name, surname, password, email):
    conn = sqlite3.connect(r"/financial_tracker\fi.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user (name, surname, password, email) VALUES (?, ?, ?, ?)",
                   (name, surname, password, email))
    conn.commit()
    conn.close()
    print("User added")

def update_password(user_id, new_password):
    conn = sqlite3.connect(r"/financial_tracker/fi.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE user SET password = ? WHERE id = ?", (new_password, user_id))
    conn.commit()
    conn.close()
    print("Password updated")


if __name__ == "__main__":
    show_users()
    add_user("Test", "User", "pass123", "testuser@example.com")
    update_password(1, "newpass123")
    show_users()
