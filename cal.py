import tkinter as tk
from tkinter import messagebox
import sqlite3
import webbrowser
import os

# Function to create the database and table if not already created
def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Function to handle user sign up
def sign_up():
    username = signup_username_entry.get()
    password = signup_password_entry.get()

    if username and password:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        existing_user = c.fetchone()

        if existing_user:
            messagebox.showerror("Sign Up Failed", "Username already exists.")
        else:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Sign Up Successful", "Account created successfully!")
            signup_window.withdraw()
            login_window.deiconify()

        conn.close()
    else:
        messagebox.showerror("Sign Up Failed", "Please fill in both fields.")

# Function to handle user login
def login():
    username = login_username_entry.get()
    password = login_password_entry.get()

    if username and password:
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            conn.close()
            open_dashboard(username)  # Open user-specific dashboard
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
            conn.close()
    else:
        messagebox.showerror("Login Failed", "Please fill in both fields.")

# Function to open user-specific HTML dashboard
def open_dashboard(username):
    # Path to save the HTML file
    html_file_path = f"{username}_dashboard.html"

    # Create HTML content dynamically
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{username}'s Dashboard</title>
    </head>
    <body>
        <h1 >Welcome, <span style="color:red;"> {username}! </span> </h1>
        <p>This is your personal dashboard.</p>
        <p>You can add more user-specific information here.</p>
    </body>
    </html>
    """

    # Write the HTML content to a file
    with open(html_file_path, "w") as html_file:
        html_file.write(html_content)

    # Open the HTML file in the default web browser
    webbrowser.open(f"file://{os.path.abspath(html_file_path)}")

# Main GUI Setup
root = tk.Tk()
root.title("User Management System")

# Creating the login window
login_window = tk.Toplevel(root)
login_window.title("Login")
login_window.geometry("300x200")
login_window.withdraw()

# Creating the sign up window
signup_window = tk.Toplevel(root)
signup_window.title("Sign Up")
signup_window.geometry("300x250")

# Sign Up Form
signup_username_label = tk.Label(signup_window, text="Username:")
signup_username_label.grid(row=0, column=0, padx=10, pady=10)

signup_username_entry = tk.Entry(signup_window, width=30)
signup_username_entry.grid(row=0, column=1, padx=10, pady=10)

signup_password_label = tk.Label(signup_window, text="Password:")
signup_password_label.grid(row=1, column=0, padx=10, pady=10)

signup_password_entry = tk.Entry(signup_window, width=30, show="*")
signup_password_entry.grid(row=1, column=1, padx=10, pady=10)

signup_button = tk.Button(signup_window, text="Sign Up", command=sign_up)
signup_button.grid(row=2, column=0, columnspan=2, pady=20)

already_have_account_label = tk.Label(signup_window, text="Already have an account?")
already_have_account_label.grid(row=3, column=0, columnspan=2)

login_button_in_signup = tk.Button(signup_window, text="Login", command=lambda: [signup_window.withdraw(), login_window.deiconify()])
login_button_in_signup.grid(row=4, column=0, columnspan=2)

# Login Form
login_username_label = tk.Label(login_window, text="Username:")
login_username_label.grid(row=0, column=0, padx=10, pady=10)

login_username_entry = tk.Entry(login_window, width=30)
login_username_entry.grid(row=0, column=1, padx=10, pady=10)

login_password_label = tk.Label(login_window, text="Password:")
login_password_label.grid(row=1, column=0, padx=10, pady=10)

login_password_entry = tk.Entry(login_window, width=30, show="*")
login_password_entry.grid(row=1, column=1, padx=10, pady=10)

login_button = tk.Button(login_window, text="Login", command=login)
login_button.grid(row=2, column=0, columnspan=2, pady=20)

no_account_label = tk.Label(login_window, text="Don't have an account?")
no_account_label.grid(row=3, column=0, columnspan=2)

signup_button_in_login = tk.Button(login_window, text="Sign Up", command=lambda: [login_window.withdraw(), signup_window.deiconify()])
signup_button_in_login.grid(row=4, column=0, columnspan=2)

# Initialize the database
create_db()

# Start the Tkinter event loop
root.mainloop()
