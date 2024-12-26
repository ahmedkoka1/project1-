import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("university_system.db") #this code to connect with data_base about  object conn
    cursor = conn.cursor()  #to use to implement the sql code 
    
    # Create tables if they don't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        major TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        description TEXT NOT NULL)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        student_id INTEGER NOT NULL,
                        course_id INTEGER NOT NULL,
                        FOREIGN KEY(student_id) REFERENCES students(id),
                        FOREIGN KEY(course_id) REFERENCES courses(id))''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS departments (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        head TEXT NOT NULL)''')
    # Extend setup_database to create the schedule table
    cursor.execute('''CREATE TABLE IF NOT EXISTS schedule (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    day TEXT NOT NULL,
                    time INTEGER NOT NULL,
                    venue TEXT NOT NULL,
                    FOREIGN KEY(course_id) REFERENCES courses(id))''')

    
    conn.commit()#if you add and delete data using sql commande ensure that the change are saved permenantly in database 
    conn.close()

# Functionality

def delete_student():
    def delete():
        student_id = entry_id.get() #this return student_id in GUI and stored in student_id 
        #if student_id isnot exist show massege error and stop this operation by return 
        if not student_id:
            messagebox.showerror("Error", "Student ID is required!")
            return
        
        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()

        # Check if the student exists
        # check if the student exists and return all data specialise by students 
        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        student = cursor.fetchone() #this code use to return first resutlt 
        
        if not student:  # if student is null show massege error and stop with return 
            messagebox.showerror("Error", "Student ID not found!")
            conn.close()
            return

        # Delete the student enrollment records
        cursor.execute("DELETE FROM enrollments WHERE student_id = ?", (student_id,))
        
        # Delete the student
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student and their enrollment records deleted successfully!")
        delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Student")

    tk.Label(delete_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(delete_window)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(delete_window, text="Delete", command=delete).grid(row=1, column=0, columnspan=2, pady=10)

def add_student():
    def save_student():
        name = entry_name.get()
        age = entry_age.get()
        major = entry_major.get()
        course_id = course_var.get()

        if not name or not age or not major or not course_id:
            messagebox.showerror("Error", "All fields are required!")
            return

        # Insert student into students table
        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, int(age), major))
        student_id = cursor.lastrowid  # Get the last inserted student ID
        
        # Enroll student in selected course
        cursor.execute("INSERT INTO enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student added and enrolled in course successfully!")
        add_window.destroy()

    # Create the add student window
    add_window = tk.Toplevel(root)
    add_window.title("Add Student")

    tk.Label(add_window, text="Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Age:").grid(row=1, column=0, padx=10, pady=10)
    entry_age = tk.Entry(add_window)
    entry_age.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Major:").grid(row=2, column=0, padx=10, pady=10)
    entry_major = tk.Entry(add_window)
    entry_major.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Select Course:").grid(row=3, column=0, padx=10, pady=10)
    
    # Get all courses from the database
    conn = sqlite3.connect("university_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    conn.close()

    # Create a dropdown menu for selecting a course
    course_var = tk.StringVar()
    course_menu = tk.OptionMenu(add_window, course_var, *[course[0] for course in courses])
    course_menu.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(add_window, text="Save", command=save_student).grid(row=4, column=0, columnspan=2, pady=10)

def delete_student():
    def delete():
        student_id = entry_id.get()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required!")
            return

        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Student deleted successfully!")
        delete_window.destroy()

    delete_window = tk.Toplevel(root)
    delete_window.title("Delete Student")

    tk.Label(delete_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_id = tk.Entry(delete_window)
    entry_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(delete_window, text="Delete", command=delete).grid(row=1, column=0, columnspan=2, pady=10)

def view_students():
    conn = sqlite3.connect("university_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    records = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel(root)
    view_window.title("View Students")

    tk.Label(view_window, text="ID", width=10).grid(row=0, column=0)
    tk.Label(view_window, text="Name", width=20).grid(row=0, column=1)
    tk.Label(view_window, text="Age", width=10).grid(row=0, column=2)
    tk.Label(view_window, text="Major", width=20).grid(row=0, column=3)

    for i, record in enumerate(records, start=1):
        tk.Label(view_window, text=record[0], width=10).grid(row=i, column=0)
        tk.Label(view_window, text=record[1], width=20).grid(row=i, column=1)
        tk.Label(view_window, text=record[2], width=10).grid(row=i, column=2)
        tk.Label(view_window, text=record[3], width=20).grid(row=i, column=3)

def add_course():
    def save_course():
        name = entry_name.get()
        description = entry_description.get()

        if not name or not description:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Course added successfully!")
        add_window.destroy()

    add_window = tk.Toplevel(root)
    add_window.title("Add Course")

    tk.Label(add_window, text="Course Name:").grid(row=0, column=0, padx=10, pady=10)
    entry_name = tk.Entry(add_window)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Description:").grid(row=1, column=0, padx=10, pady=10)
    entry_description = tk.Entry(add_window)
    entry_description.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(add_window, text="Save", command=save_course).grid(row=2, column=0, columnspan=2, pady=10)

def show_courses_for_student():
    def view_courses():
        student_id = entry_student_id.get()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required!")
            return
        
        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT c.name, c.description FROM courses c
                          JOIN enrollments e ON c.id = e.course_id
                          WHERE e.student_id = ?''', (student_id,))
        courses = cursor.fetchall()
        conn.close()

        if not courses:
            messagebox.showinfo("No Courses", "This student is not enrolled in any courses.")
            return

        view_window = tk.Toplevel(root)
        view_window.title(f"Courses for Student {student_id}")

        tk.Label(view_window, text="Course Name", width=20).grid(row=0, column=0)
        tk.Label(view_window, text="Description", width=30).grid(row=0, column=1)

        for i, course in enumerate(courses, start=1):
            tk.Label(view_window, text=course[0], width=20).grid(row=i, column=0)
            tk.Label(view_window, text=course[1], width=30).grid(row=i, column=1)

    view_window = tk.Toplevel(root)
    view_window.title("Show Courses for Student")

    tk.Label(view_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
    entry_student_id = tk.Entry(view_window)
    entry_student_id.grid(row=0, column=1, padx=10, pady=10)

    tk.Button(view_window, text="Show Courses", command=view_courses).grid(row=1, column=0, columnspan=2, pady=10)
def add_schedule():
    def save_schedule():
        course_id = course_var.get()
        day = entry_day.get()
        time = entry_time.get()
        venue = entry_venue.get()

        if not course_id or not day or not time or not venue:
            messagebox.showerror("Error", "All fields are required!")
            return

        conn = sqlite3.connect("university_system.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO schedule (course_id, day, time, venue) VALUES (?, ?, ?, ?)", (course_id, day, time, venue))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Schedule added successfully!")
        add_window.destroy()

    # Create the add schedule window
    add_window = tk.Toplevel(root)
    add_window.title("Add Schedule")

    tk.Label(add_window, text="Select Course:").grid(row=0, column=0, padx=10, pady=10)
    
    # Get all courses from the database
    conn = sqlite3.connect("university_system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM courses")
    courses = cursor.fetchall()
    conn.close()

    # Create a dropdown menu for selecting a course
    course_var = tk.StringVar()
    course_menu = tk.OptionMenu(add_window, course_var, *[course[0] for course in courses])
    course_menu.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Day:").grid(row=1, column=0, padx=10, pady=10)
    entry_day = tk.Entry(add_window)
    entry_day.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Time:").grid(row=2, column=0, padx=10, pady=10)
    entry_time = tk.Entry(add_window)
    entry_time.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(add_window, text="Venue:").grid(row=3, column=0, padx=10, pady=10)
    entry_venue = tk.Entry(add_window)
    entry_venue.grid(row=3, column=1, padx=10, pady=10)

    tk.Button(add_window, text="Save", command=save_schedule).grid(row=4, column=0, columnspan=2, pady=10)
def view_schedules():
    conn = sqlite3.connect("university_system.db")
    cursor = conn.cursor()
    cursor.execute('''SELECT s.id, c.name, s.day, s.time, s.venue 
                      FROM schedule s
                      JOIN courses c ON s.course_id = c.id''')
    records = cursor.fetchall()
    conn.close()

    view_window = tk.Toplevel(root)
    view_window.title("View Schedules")

    tk.Label(view_window, text="ID", width=10).grid(row=0, column=0)
    tk.Label(view_window, text="Course", width=20).grid(row=0, column=1)
    tk.Label(view_window, text="Day", width=10).grid(row=0, column=2)
    tk.Label(view_window, text="Time", width=10).grid(row=0, column=3)
    tk.Label(view_window, text="Venue", width=20).grid(row=0, column=4)

    for i, record in enumerate(records, start=1):
        tk.Label(view_window, text=record[0], width=10).grid(row=i, column=0)
        tk.Label(view_window, text=record[1], width=20).grid(row=i, column=1)
        tk.Label(view_window, text=record[2], width=10).grid(row=i, column=2)
        tk.Label(view_window, text=record[3], width=10).grid(row=i, column=3)
        tk.Label(view_window, text=record[4], width=20).grid(row=i, column=4)

# Main GUI
root = tk.Tk()
root.title("University System")
root.geometry("600x500")

# Database setup
setup_database()

# Heading
heading = tk.Label(root, text="University System", font=("Arial", 20))
heading.pack(pady=20)

# Student Management Frame
student_frame = tk.LabelFrame(root, text="Student Management", padx=10, pady=10)
student_frame.pack(fill="both", expand="yes", padx=20, pady=10)

btn_add_student = tk.Button(student_frame, text="Add Student", command=add_student)
btn_add_student.pack(side="left", padx=10)

btn_view_students = tk.Button(student_frame, text="View Students", command=view_students)
btn_view_students.pack(side="left", padx=10)

btn_delete_student = tk.Button(student_frame, text="Delete Student", command=delete_student)
btn_delete_student.pack(side="left", padx=10)

btn_show_courses = tk.Button(student_frame, text="Show Courses for Student", command=show_courses_for_student)
btn_show_courses.pack(side="left", padx=10)

# Course Management Frame
course_frame = tk.LabelFrame(root, text="Course Management", padx=10, pady=10)
course_frame.pack(fill="both", expand="yes", padx=20, pady=10)

btn_add_course = tk.Button(course_frame, text="Add Course", command=add_course)
btn_add_course.pack(side="left", padx=10)

# Schedule Management Frame
schedule_frame = tk.LabelFrame(root, text="Schedule Management", padx=10, pady=10)
schedule_frame.pack(fill="both", expand="yes", padx=20, pady=10)

btn_add_schedule = tk.Button(schedule_frame, text="Add Schedule", command=add_schedule)
btn_add_schedule.pack(side="left", padx=10)

btn_view_schedules = tk.Button(schedule_frame, text="View Schedules", command=view_schedules)
btn_view_schedules.pack(side="left", padx=10)

# Run the GUI
root.mainloop()
