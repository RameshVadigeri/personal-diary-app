import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import hashlib
from datetime import date

PASSWORD_FILE = "password.txt"
DIARY_DIR = "diary_entries"

if not os.path.exists(DIARY_DIR):
    os.makedirs(DIARY_DIR)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_password(pwd):
    with open(PASSWORD_FILE, "w") as f:
        f.write(hash_password(pwd))

def check_password(pwd):
    if not os.path.exists(PASSWORD_FILE):
        return False
    with open(PASSWORD_FILE, "r") as f:
        saved_hash = f.read()
    return hash_password(pwd) == saved_hash

def save_entry(entry_text):
    today = date.today().isoformat()
    filepath = os.path.join(DIARY_DIR, f"{today}.txt")
    with open(filepath, "w") as f:
        f.write(entry_text)
    messagebox.showinfo("Saved", f"Diary entry for {today} saved.")

def load_entry(entry_date):
    filepath = os.path.join(DIARY_DIR, f"{entry_date}.txt")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return f.read()
    else:
        return ""

class DiaryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Personal Diary App")
        self.create_login_ui()

    def create_login_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        tk.Label(self.master, text="Enter Password:", font=("Arial", 12)).pack(pady=10)
        self.pwd_entry = tk.Entry(self.master, show="*", width=30)
        self.pwd_entry.pack()
        tk.Button(self.master, text="Login", command=self.login).pack(pady=5)

        if not os.path.exists(PASSWORD_FILE):
            tk.Label(self.master, text="No password found. Set new password:", fg="red").pack(pady=5)
            tk.Button(self.master, text="Set Password", command=self.set_password).pack()

    def set_password(self):
        pwd = self.pwd_entry.get()
        if pwd:
            save_password(pwd)
            messagebox.showinfo("Success", "Password set successfully.")
        else:
            messagebox.showerror("Error", "Password cannot be empty.")

    def login(self):
        pwd = self.pwd_entry.get()
        if check_password(pwd):
            self.create_diary_ui()
        else:
            messagebox.showerror("Error", "Incorrect password.")

    def create_diary_ui(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        tk.Label(self.master, text="Today's Entry:", font=("Arial", 12)).pack(pady=5)
        self.text_area = scrolledtext.ScrolledText(self.master, width=50, height=15)
        self.text_area.pack()
        today = date.today().isoformat()
        self.text_area.insert(tk.END, load_entry(today))

        tk.Button(self.master, text="Save Entry", command=self.save_today).pack(pady=10)
        tk.Label(self.master, text="View Entry by Date (YYYY-MM-DD):").pack(pady=5)
        self.date_entry = tk.Entry(self.master, width=20)
        self.date_entry.pack()
        tk.Button(self.master, text="Load Entry", command=self.load_past_entry).pack(pady=5)

    def save_today(self):
        text = self.text_area.get("1.0", tk.END).strip()
        save_entry(text)

    def load_past_entry(self):
        entry_date = self.date_entry.get()
        content = load_entry(entry_date)
        if content:
            messagebox.showinfo(f"Entry for {entry_date}", content)
        else:
            messagebox.showwarning("Not Found", f"No entry for {entry_date} found.")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("500x500")
    app = DiaryApp(root)
    root.mainloop()
