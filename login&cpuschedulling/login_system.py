import tkinter as tk
from tkinter import messagebox
import sqlite3
import main_menu

DATABASE_FILE = "users.db"

# =========================
# BUTTON STYLE (GLOBAL)
# =========================
BUTTON_STYLE = {
    "bg": "#add8e6",   # light blue
    "width": 30,
    "height": 2
}

# =========================
# DATABASE INIT
# =========================
def initialize_database():
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            security_question TEXT NOT NULL,
            security_answer TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


# =========================
# LOGIN FUNCTION
# =========================
def login():
    username = entry_username.get()
    password = entry_password.get()

    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()

    if result and result[0] == password:
        messagebox.showinfo("Success", f"Welcome {username}!")
        root.withdraw()
        main_menu.open_main_menu()
    else:
        messagebox.showerror("Error", "Incorrect username or password")


# =========================
# SIGN UP WINDOW
# =========================
def open_signup():
    signup_win = tk.Toplevel(root)
    signup_win.title("Sign Up")
    signup_win.geometry("400x350")

    tk.Label(signup_win, text="Username").pack()
    entry_user = tk.Entry(signup_win)
    entry_user.pack()

    tk.Label(signup_win, text="Password").pack()
    entry_pass = tk.Entry(signup_win, show="*")
    entry_pass.pack()

    tk.Label(signup_win, text="Security Question").pack()
    entry_q = tk.Entry(signup_win)
    entry_q.pack()

    tk.Label(signup_win, text="Answer").pack()
    entry_a = tk.Entry(signup_win)
    entry_a.pack()

    def save_user():
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()

        cursor.execute("SELECT username FROM users WHERE username = ?", (entry_user.get(),))
        if cursor.fetchone():
            messagebox.showerror("Error", "User already exists")
            return

        cursor.execute('''
            INSERT INTO users VALUES (?, ?, ?, ?)
        ''', (entry_user.get(), entry_pass.get(), entry_q.get(), entry_a.get()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account created!")
        signup_win.destroy()

    tk.Button(signup_win, text="Create Account", command=save_user, **BUTTON_STYLE).pack(pady=10)

    # ENTER KEY NAVIGATION
    entry_user.bind("<Return>", lambda e: entry_pass.focus())
    entry_pass.bind("<Return>", lambda e: entry_q.focus())
    entry_q.bind("<Return>", lambda e: entry_a.focus())
    entry_a.bind("<Return>", lambda e: save_user())


# =========================
# FORGOT PASSWORD
# =========================
def forgot_password():
    forgot_win = tk.Toplevel(root)
    forgot_win.title("Forgot Password")
    forgot_win.geometry("400x350")

    tk.Label(forgot_win, text="Username").pack()
    entry_user = tk.Entry(forgot_win)
    entry_user.pack()

    def check_user():
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT security_question, security_answer FROM users WHERE username = ?", (entry_user.get(),))
        user = cursor.fetchone()
        conn.close()

        if not user:
            messagebox.showerror("Error", "User not found")
            return

        tk.Label(forgot_win, text=user[0]).pack()

        entry_ans = tk.Entry(forgot_win)
        entry_ans.pack()

        def reset_pass():
            if entry_ans.get().lower() == user[1].lower():
                new_pass = tk.Entry(forgot_win)
                new_pass.pack()

                def save_new():
                    conn = sqlite3.connect(DATABASE_FILE)
                    cursor = conn.cursor()
                    cursor.execute("UPDATE users SET password=? WHERE username=?", (new_pass.get(), entry_user.get()))
                    conn.commit()
                    conn.close()

                    messagebox.showinfo("Success", "Password updated!")
                    forgot_win.destroy()

                tk.Button(forgot_win, text="Save New Password", command=save_new, **BUTTON_STYLE).pack()

                new_pass.bind("<Return>", lambda e: save_new())

            else:
                messagebox.showerror("Error", "Wrong answer")

        tk.Button(forgot_win, text="Submit Answer", command=reset_pass, **BUTTON_STYLE).pack()
        entry_ans.bind("<Return>", lambda e: reset_pass())

    tk.Button(forgot_win, text="Next", command=check_user, **BUTTON_STYLE).pack(pady=10)
    entry_user.bind("<Return>", lambda e: check_user())


# =========================
# MAIN WINDOW
# =========================
root = tk.Tk()
root.title("Login System")
root.geometry("400x300")

initialize_database()

tk.Label(root, text="Login System", font=("Arial", 14, "bold")).pack(pady=10)

tk.Label(root, text="Username").pack()
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password").pack()
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login, **BUTTON_STYLE).pack(pady=5)
tk.Button(root, text="Sign Up", command=open_signup, **BUTTON_STYLE).pack(pady=5)
tk.Button(root, text="Forgot Password", command=forgot_password, **BUTTON_STYLE).pack(pady=5)

# ENTER KEY NAVIGATION (MAIN LOGIN)
entry_username.bind("<Return>", lambda e: entry_password.focus())
entry_password.bind("<Return>", lambda e: login())

root.mainloop()