import sqlite3
from tkinter import *
from tkinter import messagebox

# Create or connect to database
conn = sqlite3.connect('database/attendance.db')
cursor = conn.cursor()

# Create tables if not already created
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        student_id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        attendance_id INTEGER PRIMARY KEY,
        student_id INTEGER,
        date TEXT NOT NULL,
        status TEXT NOT NULL,
        FOREIGN KEY (student_id) REFERENCES students(student_id)
    );
''')
conn.commit()

# Function to add student
def add_student():
    name = entry_name.get()
    if name:
        cursor.execute('INSERT INTO students (name) VALUES (?)', (name,))
        conn.commit()
        messagebox.showinfo("Success", f"Student {name} added successfully!")
        entry_name.delete(0, END)
        update_student_list()
    else:
        messagebox.showerror("Error", "Please enter a name!")

# Function to update student list
def update_student_list():
    listbox_students.delete(0, END)
    cursor.execute('SELECT * FROM students')
    students = cursor.fetchall()
    for student in students:
        listbox_students.insert(END, f"{student[0]} - {student[1]}")

# Function to mark attendance
def mark_attendance():
    selected_student = listbox_students.curselection()
    if selected_student:
        student_id = listbox_students.get(selected_student[0]).split(' - ')[0]
        date = entry_date.get()
        status = var_status.get()
        cursor.execute('INSERT INTO attendance (student_id, date, status) VALUES (?, ?, ?)',
                       (student_id, date, status))
        conn.commit()
        messagebox.showinfo("Success", "Attendance marked successfully!")
        update_attendance_list()
    else:
        messagebox.showerror("Error", "Please select a student.")

# Function to update attendance list
def update_attendance_list():
    listbox_attendance.delete(0, END)
    cursor.execute('SELECT attendance_id, student_id, date, status FROM attendance')
    attendance_records = cursor.fetchall()
    for record in attendance_records:
        cursor.execute('SELECT name FROM students WHERE student_id = ?', (record[1],))
        student_name = cursor.fetchone()[0]
        listbox_attendance.insert(END, f"{student_name} - {record[2]} - {record[3]}")

# Set up the main window
root = Tk()
root.title("Attendance Management System")
root.geometry("600x500")

# Add student section
frame_add_student = LabelFrame(root, text="Add Student", padx=10, pady=10)
frame_add_student.pack(pady=10, padx=10, fill="both")
label_name = Label(frame_add_student, text="Student Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = Entry(frame_add_student)
entry_name.grid(row=0, column=1, padx=10, pady=5)
button_add_student = Button(frame_add_student, text="Add Student", command=add_student)
button_add_student.grid(row=0, column=2, padx=10, pady=5)

# Student list display section
frame_student_list = LabelFrame(root, text="Student List", padx=10, pady=10)
frame_student_list.pack(pady=10, padx=10, fill="both")
listbox_students = Listbox(frame_student_list, height=6, width=40)
listbox_students.grid(row=0, column=0, padx=10, pady=5)
update_student_list()

# Mark attendance section
frame_mark_attendance = LabelFrame(root, text="Mark Attendance", padx=10, pady=10)
frame_mark_attendance.pack(pady=10, padx=10, fill="both")
label_date = Label(frame_mark_attendance, text="Date (YYYY-MM-DD):")
label_date.grid(row=0, column=0, padx=10, pady=5)
entry_date = Entry(frame_mark_attendance)
entry_date.grid(row=0, column=1, padx=10, pady=5)

var_status = StringVar()
var_status.set("Present")
radio_present = Radiobutton(frame_mark_attendance, text="Present", variable=var_status, value="Present")
radio_present.grid(row=1, column=0, padx=10, pady=5)
radio_absent = Radiobutton(frame_mark_attendance, text="Absent", variable=var_status, value="Absent")
radio_absent.grid(row=1, column=1, padx=10, pady=5)
button_mark_attendance = Button(frame_mark_attendance, text="Mark Attendance", command=mark_attendance)
button_mark_attendance.grid(row=1, column=2, padx=10, pady=5)

# Attendance list section
frame_attendance_list = LabelFrame(root, text="Attendance List", padx=10, pady=10)
frame_attendance_list.pack(pady=10, padx=10, fill="both")
listbox_attendance = Listbox(frame_attendance_list, height=6, width=50)
listbox_attendance.grid(row=0, column=0, padx=10, pady=5)
update_attendance_list()

# Run the application
root.mainloop()

# Close the database connection
conn.close()
