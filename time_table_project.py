import csv
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

# File where timetables are stored
CSV_FILE = 'class_timetables.csv'

# Hardcoded admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"

# Helper function to display all timetables
def display_timetables():
    if not os.path.exists(CSV_FILE):
        messagebox.showinfo("No Data", "No timetables found.")
        return
    
    timetables = ""
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timetables += f"Class ID: {row[0]}, Class Name: {row[1]}, Subject: {row[2]}, Day: {row[3]}, Time: {row[4]}, Instructor: {row[5]}\n"
    
    result_window = tk.Toplevel(root)
    result_window.title("View Timetables")
    result_text = tk.Text(result_window)
    result_text.insert(tk.END, timetables)
    result_text.pack()

# Function to add a new timetable
def add_timetable():
    if not is_admin:
        messagebox.showwarning("Unauthorized", "Admin access required to add a timetable.")
        return
    
    class_id = simpledialog.askstring("Input", "Enter Class ID:")
    class_name = simpledialog.askstring("Input", "Enter Class Name:")
    subject = simpledialog.askstring("Input", "Enter Subject:")
    day = simpledialog.askstring("Input", "Enter Day:")
    time_slot = simpledialog.askstring("Input", "Enter Time (Start-End):")
    instructor = simpledialog.askstring("Input", "Enter Instructor:")
    
    if class_id and class_name and subject and day and time_slot and instructor:
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([class_id, class_name, subject, day, time_slot, instructor])
        messagebox.showinfo("Success", "Timetable added successfully.")
    else:
        messagebox.showwarning("Input Error", "Please fill in all fields.")

# Function to update an existing timetable
def update_timetable():
    if not is_admin:
        messagebox.showwarning("Unauthorized", "Admin access required to update a timetable.")
        return

    class_id = simpledialog.askstring("Input", "Enter Class ID to update:")
    
    timetables = []
    found = False

    if not os.path.exists(CSV_FILE):
        messagebox.showinfo("No Data", "No timetables found.")
        return
    
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            timetables.append(row)

    for row in timetables:
        if row[0] == class_id:
            found = True
            new_class_name = simpledialog.askstring("Input", f"Enter new Class Name (leave blank to keep '{row[1]}'):", initialvalue=row[1])
            new_subject = simpledialog.askstring("Input", f"Enter new Subject (leave blank to keep '{row[2]}'):", initialvalue=row[2])
            new_day = simpledialog.askstring("Input", f"Enter new Day (leave blank to keep '{row[3]}'):", initialvalue=row[3])
            new_time = simpledialog.askstring("Input", f"Enter new Time (leave blank to keep '{row[4]}'):", initialvalue=row[4])
            new_instructor = simpledialog.askstring("Input", f"Enter new Instructor (leave blank to keep '{row[5]}'):", initialvalue=row[5])
            
            row[1] = new_class_name or row[1]
            row[2] = new_subject or row[2]
            row[3] = new_day or row[3]
            row[4] = new_time or row[4]
            row[5] = new_instructor or row[5]
            messagebox.showinfo("Success", "Timetable updated successfully.")
            break

    if found:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(timetables)
    else:
        messagebox.showwarning("Not Found", "Class ID not found.")

# Function to delete a timetable
def delete_timetable():
    if not is_admin:
        messagebox.showwarning("Unauthorized", "Admin access required to delete a timetable.")
        return

    class_id = simpledialog.askstring("Input", "Enter Class ID to delete:")
    
    timetables = []
    found = False

    if not os.path.exists(CSV_FILE):
        messagebox.showinfo("No Data", "No timetables found.")
        return
    
    with open(CSV_FILE, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] != class_id:
                timetables.append(row)
            else:
                found = True

    if found:
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(timetables)
        messagebox.showinfo("Success", "Timetable deleted successfully.")
    else:
        messagebox.showwarning("Not Found", "Class ID not found.")

# Admin login function
def admin_login():
    global is_admin
    username = simpledialog.askstring("Login", "Enter admin username:")
    password = simpledialog.askstring("Login", "Enter admin password:", show="*")

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        is_admin = True
        messagebox.showinfo("Login Success", "Welcome, Admin!")
    else:
        messagebox.showwarning("Login Failed", "Invalid credentials.")

# Main GUI
root = tk.Tk()
root.title("Class Timetable Management System")
root.geometry("400x300")

is_admin = False

# GUI Buttons
tk.Button(root, text="View All Timetables", command=display_timetables).pack(pady=10)
tk.Button(root, text="Add Timetable", command=add_timetable).pack(pady=10)
tk.Button(root, text="Update Timetable", command=update_timetable).pack(pady=10)
tk.Button(root, text="Delete Timetable", command=delete_timetable).pack(pady=10)
tk.Button(root, text="Admin Login", command=admin_login).pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
