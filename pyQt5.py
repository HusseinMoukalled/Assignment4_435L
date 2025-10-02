# On my honor I have neither given nor received unauthorized aid on this assignment. I used AI tools to research concepts, understand the code and get templates.

import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Person:
    """
    Base class representing a person with name, age, and email.

    :param name: Full name of the person.
    :type name: str
    :param age: Age of the person; must be a non-negative integer.
    :type age: int
    :param email: Email address in the format ``name@example.com``.
    :type email: str
    :raises ValueError: If ``age`` is negative or not an int, or if ``email`` is not in a valid format.
    """

    def __init__(self, name: str, age: int, email: str):
        """
        Initialize a :class:`Person`.

        :param name: Full name.
        :type name: str
        :param age: Non-negative integer age.
        :type age: int
        :param email: Email address.
        :type email: str
        :raises ValueError: If validation fails.
        """
        if not isinstance(age,int) or age<0:
            raise ValueError("Age must be a positive integer")
        if not isinstance(email, str) or "@" not in email or "." not in email.split('@')[-1]:
            # email.split('@')[-1] returns the domain part; we check it contains a dot.
            raise ValueError("Email must be a string of valid format: name@example.com")
        self.name=name
        self.age=age
        self._email=email  # leading underscore by convention indicates internal use

    def introduce(self):
        """
        Print a short self-introduction to stdout.

        :return: None
        :rtype: None
        """
        print(f"My name is {self.name} and I am {self.age} years old.")
        
class Student(Person):
    """
    Subclass representing a student. Inherits from :class:`Person`.

    :param name: Student's name.
    :type name: str
    :param age: Student's age.
    :type age: int
    :param email: Student's email.
    :type email: str
    :param student_id: Unique student identifier.
    :type student_id: str
    """

    def __init__(self, name: str, age: int, email: str, student_id: str):
        """
        Initialize a :class:`Student`.

        :param name: Student's name.
        :type name: str
        :param age: Student's age (non-negative integer).
        :type age: int
        :param email: Student's email.
        :type email: str
        :param student_id: Unique student ID.
        :type student_id: str
        """
        # registered_courses intentionally starts as an empty list for all students.
        super().__init__(name, age, email)
        self.student_id=student_id
        self.registered_courses=[]

    def register_course(self, course):
        """
        Register the student to a course.

        :param course: Course to register the student in.
        :type course: Course
        :raises TypeError: If ``course`` is not an instance of :class:`Course`.
        :return: None
        :rtype: None
        """
        if not isinstance(course, Course):
            raise TypeError("This course is not recognized")
        self.registered_courses.append(course)

class Instructor(Person):
    """
    Subclass representing an instructor. Inherits from :class:`Person`.

    :param name: Instructor's name.
    :type name: str
    :param age: Instructor's age.
    :type age: int
    :param email: Instructor's email.
    :type email: str
    :param instructor_id: Unique instructor identifier.
    :type instructor_id: str
    """

    def __init__(self, name: str, age: int, email: str, instructor_id: str):
        """
        Initialize an :class:`Instructor`.

        :param name: Instructor's name.
        :type name: str
        :param age: Instructor's age (non-negative integer).
        :type age: int
        :param email: Instructor's email.
        :type email: str
        :param instructor_id: Unique instructor ID.
        :type instructor_id: str
        """
        super().__init__(name, age, email)
        self.instructor_id=instructor_id
        self.assigned_courses=[]

    def assign_course(self, course):
        """
        Assign a course to this instructor.

        :param course: Course to assign.
        :type course: Course
        :raises TypeError: If ``course`` is not an instance of :class:`Course`.
        :return: None
        :rtype: None
        """
        if not isinstance(course, Course):
            raise TypeError("This course is not recognized")
        self.assigned_courses.append(course)

class Course:
    """
    Represents a course with an assigned instructor and a roster of students.

    :param course_id: Unique course identifier.
    :type course_id: str
    :param course_name: Human-readable course name.
    :type course_name: str
    :param instructor: Instructor assigned to the course.
    :type instructor: Instructor
    :raises TypeError: If ``instructor`` is not an :class:`Instructor`.
    """

    def __init__(self, course_id: str, course_name: str, instructor):
        """
        Initialize a :class:`Course`.

        :param course_id: Course ID.
        :type course_id: str
        :param course_name: Course name.
        :type course_name: str
        :param instructor: Assigned instructor.
        :type instructor: Instructor
        :raises TypeError: If instructor is not an :class:`Instructor`.
        """
        if not isinstance(instructor, Instructor):
            raise TypeError("This instructor is not recognized")
        self.course_id=course_id
        self.course_name=course_name
        self.instructor=instructor
        self.enrolled_students=[]

    def add_student(self, student):
        """
        Enroll a student into the course.

        :param student: Student to add.
        :type student: Student
        :raises TypeError: If ``student`` is not a :class:`Student`.
        :return: None
        :rtype: None
        """
        if not isinstance(student, Student):
            raise TypeError("This student is not recognized")
        self.enrolled_students.append(student)

def serialization_json(students, instructors, courses):
    """
    Serialize in-memory objects to a JSON-friendly dictionary.

    :param students: List of :class:`Student` objects.
    :type students: list
    :param instructors: List of :class:`Instructor` objects.
    :type instructors: list
    :param courses: List of :class:`Course` objects.
    :type courses: list
    :return: Dictionary with keys ``students``, ``instructors``, and ``courses``.
    :rtype: dict
    """
    data={
        "students":[],
        "instructors":[],
        "courses":[] 
    }

    for student in students:
        data['students'].append({"name": student.name, "age": student.age, "email": student._email, "student_id": student.student_id, "registered_courses": [course.course_id for course in student.registered_courses]})

    for instructor in instructors:
        data['instructors'].append({"name": instructor.name, "age": instructor.age, "email": instructor._email, "instructor_id": instructor.instructor_id, "assigned_courses": [course.course_id for course in instructor.assigned_courses]})

    for course in courses:
        data["courses"].append({"course_id": course.course_id, "course_name": course.course_name, "instructor_id":course.instructor.instructor_id, "enrolled_students": [student.student_id for student in course.enrolled_students]})

    return data

def save_to_file(filename, students, instructors, courses):
    """
    Save current data to a JSON file.

    :param filename: Destination JSON filename.
    :type filename: str
    :param students: List of :class:`Student` objects.
    :type students: list
    :param instructors: List of :class:`Instructor` objects.
    :type instructors: list
    :param courses: List of :class:`Course` objects.
    :type courses: list
    :return: None
    :rtype: None
    """
    data=serialization_json(students, instructors, courses)
    f=open(filename,"w")
    json.dump(data,f)
    print("Data successfully saved to", filename)
    f.close()

def load_from_file(filename):
    """
    Load data from a JSON file.

    :param filename: Path to JSON file.
    :type filename: str
    :return: Parsed data with keys ``students``, ``instructors``, and ``courses``.
    :rtype: dict
    :raises FileNotFoundError: If file does not exist.
    """
    f=open(filename, "r")
    data=json.load(f)
    print("Data loaded successfully from", filename)
    return data
    f.close()


import sys, csv, os, sqlite3, shutil
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QGroupBox, QComboBox, QTabWidget,
    QTableWidget, QTableWidgetItem, QMessageBox, QFileDialog
)
from PyQt5.QtCore import Qt

DB_PATH = "school.db"
"""Default path to the SQLite database file used by the application."""

def init_db(db_path=DB_PATH):
    """
    Initialize the SQLite database, creating tables if they do not exist.

    Tables: ``students``, ``instructors``, ``courses``, ``enrollments``.

    :param db_path: Path to the SQLite DB file.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS students(
        student_id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS instructors(
        instructor_id TEXT PRIMARY KEY, name TEXT, age INTEGER, email TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS courses(
        course_id TEXT PRIMARY KEY, course_name TEXT, instructor_id TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS enrollments(
        student_id TEXT, course_id TEXT,
        UNIQUE(student_id, course_id) ON CONFLICT IGNORE)""")
    con.commit(); con.close()

def db_fetch_all(db_path=DB_PATH):
    """
    Fetch all rows from all tables.

    :param db_path: Path to the SQLite DB file.
    :type db_path: str
    :return: Dictionary with keys ``students``, ``instructors``, ``courses``, ``enrollments``; each value is a list of tuples.
    :rtype: dict
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("SELECT student_id,name,age,email FROM students"); students = cur.fetchall()
    cur.execute("SELECT instructor_id,name,age,email FROM instructors"); instructors = cur.fetchall()
    cur.execute("SELECT course_id,course_name,instructor_id FROM courses"); courses = cur.fetchall()
    cur.execute("SELECT student_id,course_id FROM enrollments"); enrollments = cur.fetchall()
    con.close()
    return {"students": students, "instructors": instructors, "courses": courses, "enrollments": enrollments}

def backup_db(src=DB_PATH, dst="school_backup.db"):
    """
    Create a file copy of the database.

    :param src: Source database path.
    :type src: str
    :param dst: Destination backup filename.
    :type dst: str
    :return: Absolute path of the backup file.
    :rtype: str
    """
    shutil.copyfile(src, dst)
    return os.path.abspath(dst)

def db_add_student(sid, name, age, email, db_path=DB_PATH):
    """
    Insert or replace a student record.

    :param sid: Student ID.
    :type sid: str
    :param name: Student name.
    :type name: str
    :param age: Student age.
    :type age: int
    :param email: Student email.
    :type email: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO students VALUES (?,?,?,?)", (sid, name, age, email))
    con.commit(); con.close()

def db_update_student(sid, name, age, email, db_path=DB_PATH):
    """
    Update a student record by ID.

    :param sid: Student ID.
    :type sid: str
    :param name: New name.
    :type name: str
    :param age: New age.
    :type age: int
    :param email: New email.
    :type email: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?", (name, age, email, sid))
    con.commit(); con.close()

def db_delete_student(sid, db_path=DB_PATH):
    """
    Delete a student and related enrollments.

    :param sid: Student ID to delete.
    :type sid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("DELETE FROM enrollments WHERE student_id=?", (sid,))
    cur.execute("DELETE FROM students WHERE student_id=?", (sid,))
    con.commit(); con.close()

def db_add_instructor(iid, name, age, email, db_path=DB_PATH):
    """
    Insert or replace an instructor record.

    :param iid: Instructor ID.
    :type iid: str
    :param name: Name.
    :type name: str
    :param age: Age.
    :type age: int
    :param email: Email.
    :type email: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO instructors VALUES (?,?,?,?)", (iid, name, age, email))
    con.commit(); con.close()

def db_update_instructor(iid, name, age, email, db_path=DB_PATH):
    """
    Update an instructor by ID.

    :param iid: Instructor ID.
    :type iid: str
    :param name: New name.
    :type name: str
    :param age: New age.
    :type age: int
    :param email: New email.
    :type email: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?", (name, age, email, iid))
    con.commit(); con.close()

def db_delete_instructor(iid, db_path=DB_PATH):
    """
    Delete an instructor if they have no assigned courses.

    :param iid: Instructor ID.
    :type iid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM courses WHERE instructor_id=?", (iid,))
    if cur.fetchone()[0] == 0:
        cur.execute("DELETE FROM instructors WHERE instructor_id=?", (iid,))
    con.commit(); con.close()

def db_add_course(cid, cname, iid, db_path=DB_PATH):
    """
    Insert or replace a course.

    :param cid: Course ID.
    :type cid: str
    :param cname: Course name.
    :type cname: str
    :param iid: Instructor ID.
    :type iid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("INSERT OR REPLACE INTO courses VALUES (?,?,?)", (cid, cname, iid))
    con.commit(); con.close()

def db_update_course(cid, cname, iid, db_path=DB_PATH):
    """
    Update a course by ID.

    :param cid: Course ID.
    :type cid: str
    :param cname: New course name.
    :type cname: str
    :param iid: New instructor ID.
    :type iid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("UPDATE courses SET course_name=?, instructor_id=? WHERE course_id=?", (cname, iid, cid))
    con.commit(); con.close()

def db_delete_course(cid, db_path=DB_PATH):
    """
    Delete a course and its enrollments.

    :param cid: Course ID.
    :type cid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("DELETE FROM enrollments WHERE course_id=?", (cid,))
    cur.execute("DELETE FROM courses WHERE course_id=?", (cid,))
    con.commit(); con.close()

def db_enroll(sid, cid, db_path=DB_PATH):
    """
    Enroll a student into a course (no duplicates).

    :param sid: Student ID.
    :type sid: str
    :param cid: Course ID.
    :type cid: str
    :param db_path: DB path.
    :type db_path: str
    :return: None
    :rtype: None
    """
    con = sqlite3.connect(db_path); cur = con.cursor()
    cur.execute("INSERT OR IGNORE INTO enrollments(student_id,course_id) VALUES (?,?)", (sid, cid))
    con.commit(); con.close()


students: list = []
"""In-memory list of :class:`Student` objects currently loaded in the UI."""

instructors: list = []
"""In-memory list of :class:`Instructor` objects currently loaded in the UI."""

courses: list = []
"""In-memory list of :class:`Course` objects currently loaded in the UI."""

def find_student(sid):
    """
    Find a student object by ID in the in-memory list.

    :param sid: Student ID.
    :type sid: str
    :return: The matching :class:`Student` or ``None`` if not found.
    :rtype: Student | None
    """
    return next((s for s in students if s.student_id == sid), None)

def find_instructor(iid):
    """
    Find an instructor object by ID in the in-memory list.

    :param iid: Instructor ID.
    :type iid: str
    :return: The matching :class:`Instructor` or ``None`` if not found.
    :rtype: Instructor | None
    """
    return next((i for i in instructors if i.instructor_id == iid), None)

def find_course(cid):
    """
    Find a course object by ID in the in-memory list.

    :param cid: Course ID.
    :type cid: str
    :return: The matching :class:`Course` or ``None`` if not found.
    :rtype: Course | None
    """
    return next((c for c in courses if c.course_id == cid), None)

def email_ok(e: str) -> bool:
    """
    Validate a simple email format.

    :param e: Email string to validate.
    :type e: str
    :return: ``True`` if the email looks valid, else ``False``.
    :rtype: bool
    """
    return isinstance(e, str) and "@" in e and "." in e.split("@")[-1]

def alert(parent, title, text):
    """
    Show an information dialog.

    :param parent: Parent widget.
    :type parent: QWidget
    :param title: Dialog title.
    :type title: str
    :param text: Message text.
    :type text: str
    :return: None
    :rtype: None
    """
    QMessageBox.information(parent, title, text)

def error(parent, title, text):
    """
    Show an error dialog.

    :param parent: Parent widget.
    :type parent: QWidget
    :param title: Dialog title.
    :type title: str
    :param text: Error message text.
    :type text: str
    :return: None
    :rtype: None
    """
    QMessageBox.critical(parent, title, text)


class MainWindow(QMainWindow):
    """
    Main window of the School Management System built with PyQt5.

    Provides forms for adding/updating students, instructors, and courses,
    along with search/filtering, JSON import/export, CSV export, database
    backup, and enrollment/assignment actions.
    """

    def __init__(self):
        """
        Construct the main window, build the UI, and load existing data from DB.

        :return: None
        :rtype: None
        """
        super().__init__()
        self.setWindowTitle("School Management System")
        self.resize(1100, 720)

        container = QWidget(); self.setCentralWidget(container)
        outer = QVBoxLayout(container)
        forms_row = QHBoxLayout(); outer.addLayout(forms_row)
        self.stu_name, self.stu_age, self.stu_email, self.stu_id = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        stu_box = QGroupBox("Add / Edit Student"); g = QGridLayout(stu_box)
        g.addWidget(QLabel("Name"),0,0); g.addWidget(self.stu_name,0,1)
        g.addWidget(QLabel("Age"),1,0);  g.addWidget(self.stu_age,1,1)
        g.addWidget(QLabel("Email"),2,0);g.addWidget(self.stu_email,2,1)
        g.addWidget(QLabel("Student ID"),3,0); g.addWidget(self.stu_id,3,1)
        b1=QPushButton("Add Student"); b1.clicked.connect(self.add_student)
        b1u=QPushButton("Update Selected"); b1u.clicked.connect(self.update_selected_student)
        g.addWidget(b1,4,0,1,2); g.addWidget(b1u,5,0,1,2); forms_row.addWidget(stu_box)

        
        self.ins_name, self.ins_age, self.ins_email, self.ins_id = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit()
        ins_box = QGroupBox("Add / Edit Instructor"); g2 = QGridLayout(ins_box)
        g2.addWidget(QLabel("Name"),0,0); g2.addWidget(self.ins_name,0,1)
        g2.addWidget(QLabel("Age"),1,0);  g2.addWidget(self.ins_age,1,1)
        g2.addWidget(QLabel("Email"),2,0);g2.addWidget(self.ins_email,2,1)
        g2.addWidget(QLabel("Instructor ID"),3,0); g2.addWidget(self.ins_id,3,1)
        b2=QPushButton("Add Instructor"); b2.clicked.connect(self.add_instructor)
        b2u=QPushButton("Update Selected"); b2u.clicked.connect(self.update_selected_instructor)
        g2.addWidget(b2,4,0,1,2); g2.addWidget(b2u,5,0,1,2); forms_row.addWidget(ins_box)

        
        self.crs_id, self.crs_name, self.crs_inst_id = QLineEdit(), QLineEdit(), QLineEdit()
        crs_box = QGroupBox("Add / Edit Course"); g3 = QGridLayout(crs_box)
        g3.addWidget(QLabel("Course ID"),0,0);    g3.addWidget(self.crs_id,0,1)
        g3.addWidget(QLabel("Course Name"),1,0);  g3.addWidget(self.crs_name,1,1)
        g3.addWidget(QLabel("Instructor ID (must exist)"),2,0); g3.addWidget(self.crs_inst_id,2,1)
        b3=QPushButton("Add Course"); b3.clicked.connect(self.add_course)
        b3u=QPushButton("Update Selected"); b3u.clicked.connect(self.update_selected_course)
        g3.addWidget(b3,3,0,1,2); g3.addWidget(b3u,4,0,1,2); forms_row.addWidget(crs_box)

        
        middle = QHBoxLayout(); outer.addLayout(middle)

      
        reg_box = QGroupBox("Register Student in Course"); rg = QGridLayout(reg_box)
        self.reg_student, self.reg_course = QComboBox(), QComboBox()
        rg.addWidget(QLabel("Student"),0,0); rg.addWidget(self.reg_student,0,1)
        rg.addWidget(QLabel("Course"),1,0);  rg.addWidget(self.reg_course,1,1)
        br=QPushButton("Register"); br.clicked.connect(self.register_student)
        rg.addWidget(br,2,0,1,2); middle.addWidget(reg_box)

       
        asg_box = QGroupBox("Assign Instructor to Course"); ag = QGridLayout(asg_box)
        self.asg_instructor, self.asg_course = QComboBox(), QComboBox()
        ag.addWidget(QLabel("Instructor"),0,0); ag.addWidget(self.asg_instructor,0,1)
        ag.addWidget(QLabel("Course"),1,0);     ag.addWidget(self.asg_course,1,1)
        ba=QPushButton("Assign"); ba.clicked.connect(self.assign_instructor)
        ag.addWidget(ba,2,0,1,2); middle.addWidget(asg_box)

      
        ops_box = QGroupBox("Data"); op = QGridLayout(ops_box)
        self.search_line = QLineEdit()
        btn_search = QPushButton("Search"); btn_search.clicked.connect(self.refresh_tables)
        btn_clear  = QPushButton("Clear");  btn_clear.clicked.connect(lambda:(self.search_line.setText(""), self.refresh_tables()))
        btn_save   = QPushButton("Save JSON"); btn_save.clicked.connect(self.save_json)
        btn_load   = QPushButton("Load JSON"); btn_load.clicked.connect(self.load_json)
        btn_export = QPushButton("Export CSV"); btn_export.clicked.connect(self.export_csv)
        btn_loaddb = QPushButton("Load from DB"); btn_loaddb.clicked.connect(self.load_from_database)
        btn_backup = QPushButton("Backup DB"); btn_backup.clicked.connect(self.backup_database)
        op.addWidget(QLabel("Search (name / ID / course)"),0,0,1,2)
        op.addWidget(self.search_line,1,0,1,2)
        op.addWidget(btn_search,2,0); op.addWidget(btn_clear,2,1)
        op.addWidget(btn_save,3,0);   op.addWidget(btn_load,3,1)
        op.addWidget(btn_export,4,0,1,2)
        op.addWidget(btn_loaddb,5,0); op.addWidget(btn_backup,5,1)
        middle.addWidget(ops_box)

       
        bottom = QVBoxLayout(); outer.addLayout(bottom)
        tabs = QTabWidget(); bottom.addWidget(tabs, stretch=1)

        self.stu_table = QTableWidget(0,5)
        self.stu_table.setHorizontalHeaderLabels(["Student ID","Name","Age","Email","Courses"])
        self.stu_table.itemSelectionChanged.connect(self.load_student_into_form)
        tabs.addTab(self.stu_table,"Students")

        self.ins_table = QTableWidget(0,5)
        self.ins_table.setHorizontalHeaderLabels(["Instructor ID","Name","Age","Email","Assigned"])
        self.ins_table.itemSelectionChanged.connect(self.load_instructor_into_form)
        tabs.addTab(self.ins_table,"Instructors")

        self.crs_table = QTableWidget(0,4)
        self.crs_table.setHorizontalHeaderLabels(["Course ID","Course Name","Instructor ID","Enrolled"])
        self.crs_table.itemSelectionChanged.connect(self.load_course_into_form)
        tabs.addTab(self.crs_table,"Courses")

        del_row = QHBoxLayout(); bottom.addLayout(del_row)
        d1=QPushButton("Delete Selected Student"); d1.clicked.connect(self.delete_selected_student)
        d2=QPushButton("Delete Selected Instructor"); d2.clicked.connect(self.delete_selected_instructor)
        d3=QPushButton("Delete Selected Course"); d3.clicked.connect(self.delete_selected_course)
        del_row.addWidget(d1); del_row.addWidget(d2); del_row.addWidget(d3)

      
        self.load_from_database()  

  
    def load_from_database(self):
        """
        Load all records from SQLite into in-memory lists and refresh the UI.

        This synchronizes the in-memory data structures (:data:`students`,
        :data:`instructors`, :data:`courses`) with the database and updates
        the comboboxes and tables.

        :return: None
        :rtype: None
        """
        data = db_fetch_all(DB_PATH)
        students.clear(); instructors.clear(); courses.clear()

        for iid, name, age, email in data["instructors"]:
            instructors.append(Instructor(name, int(age), email, iid))
        for sid, name, age, email in data["students"]:
            students.append(Student(name, int(age), email, sid))

        iid_map = {i.instructor_id: i for i in instructors}
        for cid, cname, iid in data["courses"]:
            ins = iid_map.get(iid)
            if not ins: continue
            crs = Course(cid, cname, ins); courses.append(crs); ins.assign_course(crs)

        sid_map = {s.student_id: s for s in students}
        for sid, cid in data["enrollments"]:
            s = sid_map.get(sid); c = find_course(cid)
            if s and c:
                if s not in c.enrolled_students: c.add_student(s)
                if c not in s.registered_courses: s.register_course(c)

        self.refresh_all_dropdowns(); self.refresh_tables()
        alert(self,"DB","Loaded from SQLite.")

    def backup_database(self):
        """
        Create a backup of the SQLite database in the current directory.

        :return: None
        :rtype: None
        """
        dst = backup_db(DB_PATH, "school_backup.db")
        alert(self,"Backup",f"Database copied to:\n{dst}")

   
    def add_student(self):
        """
        Add a new student using the values from the student form fields.

        Performs basic validation (non-empty fields, integer age, email format,
        and unique student ID), inserts the record into the DB, updates the
        in-memory list, and refreshes the UI.

        :return: None
        :rtype: None
        """
        name = self.stu_name.text().strip(); sid = self.stu_id.text().strip()
        email = self.stu_email.text().strip()
        try: age = int(self.stu_age.text().strip())
        except: return error(self,"Error","Age must be an integer")
        if not name or not sid: return error(self,"Error","Name and Student ID are required")
        if not email_ok(email): return error(self,"Error","Invalid email")
        if find_student(sid): return error(self,"Error","Student ID already exists")
        try:
            s = Student(name, age, email, sid)
            students.append(s); db_add_student(sid, name, age, email)
            alert(self,"OK",f"Student '{name}' added"); self.refresh_all_dropdowns(); self.refresh_tables()
        except ValueError as e: error(self,"Error",str(e))

    def add_instructor(self):
        """
        Add a new instructor using the values from the instructor form fields.

        Validates inputs, inserts into DB, updates in-memory list, and refreshes UI.

        :return: None
        :rtype: None
        """
        name = self.ins_name.text().strip(); iid = self.ins_id.text().strip()
        email = self.ins_email.text().strip()
        try: age = int(self.ins_age.text().strip())
        except: return error(self,"Error","Age must be an integer")
        if not name or not iid: return error(self,"Error","Name and Instructor ID are required")
        if not email_ok(email): return error(self,"Error","Invalid email")
        if find_instructor(iid): return error(self,"Error","Instructor ID already exists")
        try:
            i = Instructor(name, age, email, iid)
            instructors.append(i); db_add_instructor(iid, name, age, email)
            alert(self,"OK",f"Instructor '{name}' added"); self.refresh_all_dropdowns(); self.refresh_tables()
        except ValueError as e: error(self,"Error",str(e))

    def add_course(self):
        """
        Add a new course using the values from the course form fields.

        Requires an existing instructor ID. Inserts into DB, updates in-memory list,
        and refreshes the UI.

        :return: None
        :rtype: None
        """
        cid = self.crs_id.text().strip(); cname = self.crs_name.text().strip()
        iid = self.crs_inst_id.text().strip()
        if not cid or not cname or not iid: return error(self,"Error","Course ID, Name, and Instructor ID are required")
        inst = find_instructor(iid); 
        if not inst: return error(self,"Error","Instructor not found")
        if find_course(cid): return error(self,"Error","Course ID already exists")
        try:
            c = Course(cid, cname, inst); courses.append(c); inst.assign_course(c)
            db_add_course(cid, cname, iid)
            alert(self,"OK",f"Course '{cname}' added"); self.refresh_all_dropdowns(); self.refresh_tables()
        except TypeError as e: error(self,"Error",str(e))

    
    def update_selected_student(self):
        """
        Update the currently selected student in the table based on the form fields.

        :return: None
        :rtype: None
        """
        sid = self.stu_id.text().strip(); s = find_student(sid)
        if not s: return error(self,"Error","Student not found by ID")
        try:
            s.name = self.stu_name.text().strip()
            s.age  = int(self.stu_age.text().strip())
            e = self.stu_email.text().strip()
            if not email_ok(e): return error(self,"Error","Invalid email")
            s._email = e; db_update_student(sid, s.name, s.age, s._email)
            alert(self,"OK","Student updated"); self.refresh_tables()
        except ValueError as e: error(self,"Error",str(e))

    def update_selected_instructor(self):
        """
        Update the currently selected instructor in the table based on the form fields.

        :return: None
        :rtype: None
        """
        iid = self.ins_id.text().strip(); ins = find_instructor(iid)
        if not ins: return error(self,"Error","Instructor not found by ID")
        try:
            ins.name = self.ins_name.text().strip()
            ins.age  = int(self.ins_age.text().strip())
            e = self.ins_email.text().strip()
            if not email_ok(e): return error(self,"Error","Invalid email")
            ins._email = e; db_update_instructor(iid, ins.name, ins.age, ins._email)
            alert(self,"OK","Instructor updated"); self.refresh_tables()
        except ValueError as e: error(self,"Error",str(e))

    def update_selected_course(self):
        """
        Update the currently selected course in the table based on the form fields.

        Handles reassignment of instructor if changed.

        :return: None
        :rtype: None
        """
        cid = self.crs_id.text().strip(); crs = find_course(cid)
        if not crs: return error(self,"Error","Course not found by ID")
        cname = self.crs_name.text().strip(); iid = self.crs_inst_id.text().strip()
        inst = find_instructor(iid)
        if not cname: return error(self,"Error","Course name required")
        if not inst:  return error(self,"Error","Instructor not found by ID")
        if crs.instructor != inst:
            if crs.instructor and crs in crs.instructor.assigned_courses:
                crs.instructor.assigned_courses.remove(crs)
            inst.assign_course(crs); crs.instructor = inst
        crs.course_name = cname; db_update_course(cid, cname, iid)
        alert(self,"OK","Course updated"); self.refresh_all_dropdowns(); self.refresh_tables()

    
    def delete_selected_student(self):
        """
        Delete the selected student from the table and database.

        Also removes the student from any course enrollments.

        :return: None
        :rtype: None
        """
        row = self.stu_table.currentRow()
        if row < 0: return
        sid = self.stu_table.item(row,0).text(); s = find_student(sid)
        if not s: return
        for c in courses:
            if s in c.enrolled_students: c.enrolled_students.remove(s)
        students.remove(s); db_delete_student(sid)
        alert(self,"OK",f"Deleted student {sid}"); self.refresh_all_dropdowns(); self.refresh_tables()

    def delete_selected_instructor(self):
        """
        Delete the selected instructor from the table and database if they have no assigned courses.

        :return: None
        :rtype: None
        """
        row = self.ins_table.currentRow()
        if row < 0: return
        iid = self.ins_table.item(row,0).text(); ins = find_instructor(iid)
        if not ins: return
        if ins.assigned_courses: return error(self,"Error","Cannot delete: instructor has assigned courses. Reassign first.")
        instructors.remove(ins); db_delete_instructor(iid)
        alert(self,"OK",f"Deleted instructor {iid}"); self.refresh_all_dropdowns(); self.refresh_tables()

    def delete_selected_course(self):
        """
        Delete the selected course from the table and database, cleaning up relationships.

        :return: None
        :rtype: None
        """
        row = self.crs_table.currentRow()
        if row < 0: return
        cid = self.crs_table.item(row,0).text(); crs = find_course(cid)
        if not crs: return
        if crs.instructor and crs in crs.instructor.assigned_courses:
            crs.instructor.assigned_courses.remove(crs)
        for s in students:
            if crs in s.registered_courses: s.registered_courses.remove(crs)
        courses.remove(crs); db_delete_course(cid)
        alert(self,"OK",f"Deleted course {cid}"); self.refresh_all_dropdowns(); self.refresh_tables()

  
    def register_student(self):
        """
        Register the selected student to the selected course.

        Uses combobox selections; persists the relation in DB and updates UI.

        :return: None
        :rtype: None
        """
        s_lbl = self.reg_student.currentText(); c_lbl = self.reg_course.currentText()
        if not s_lbl or not c_lbl: return
        sid = s_lbl.split(" - ",1)[0]; cid = c_lbl.split(" - ",1)[0]
        s = find_student(sid); c = find_course(cid)
        if not s or not c: return error(self,"Error","Select valid student and course")
        if s in c.enrolled_students: return alert(self,"Info",f"{s.name} is already enrolled in {c.course_name}")
        c.add_student(s); s.register_course(c); db_enroll(sid, cid)
        alert(self,"OK",f"Enrolled {s.name} in {c.course_name}"); self.refresh_tables()

    def assign_instructor(self):
        """
        Assign the selected instructor to the selected course.

        Updates the course's instructor and persists to DB.

        :return: None
        :rtype: None
        """
        i_lbl = self.asg_instructor.currentText(); c_lbl = self.asg_course.currentText()
        if not i_lbl or not c_lbl: return
        iid = i_lbl.split(" - ",1)[0]; cid = c_lbl.split(" - ",1)[0]
        ins = find_instructor(iid); crs = find_course(cid)
        if not ins or not crs: return error(self,"Error","Select valid instructor and course")
        if crs in ins.assigned_courses: return alert(self,"Info",f"{ins.name} already assigned to {crs.course_name}")
        ins.assign_course(crs); crs.instructor = ins; db_update_course(crs.course_id, crs.course_name, ins.instructor_id)
        alert(self,"OK",f"Assigned {ins.name} to {crs.course_name}"); self.refresh_all_dropdowns(); self.refresh_tables()


    def save_json(self):
        """
        Save the in-memory data to a JSON file via a file dialog.

        :return: None
        :rtype: None
        """
        path, _ = QFileDialog.getSaveFileName(self,"Save JSON","school_data.json","JSON Files (*.json)")
        if not path: return
        save_to_file(path, students, instructors, courses)
        alert(self,"Saved",f"Data saved to {path}")

    def load_json(self):
        """
        Load data from a JSON file into in-memory objects and refresh the UI.

        :return: None
        :rtype: None
        :raises FileNotFoundError: If selected file cannot be found.
        """
        path, _ = QFileDialog.getOpenFileName(self,"Load JSON","school_data.json","JSON Files (*.json)")
        if not path: return
        try: data = load_from_file(path)
        except FileNotFoundError: return error(self,"Error","File not found")

        
        students.clear(); instructors.clear(); courses.clear()
        for i in data.get("instructors",[]): instructors.append(Instructor(i["name"], i["age"], i["email"], i["instructor_id"]))
        for s in data.get("students",[]):     students.append(Student(s["name"], s["age"], s["email"], s["student_id"]))

        iid_map = {i.instructor_id:i for i in instructors}
        for c in data.get("courses",[]):
            ins = iid_map.get(c["instructor_id"])
            crs = Course(c["course_id"], c["course_name"], ins); courses.append(crs); ins.assign_course(crs)

        sid_map = {s.student_id:s for s in students}
        for c in data.get("courses",[]):
            crs = find_course(c["course_id"]); 
            if not crs: continue
            for sid in c.get("enrolled_students",[]):
                stu = sid_map.get(sid)
                if stu:
                    if stu not in crs.enrolled_students: crs.add_student(stu)
                    if crs not in stu.registered_courses: stu.register_course(crs)

        alert(self,"Loaded",f"Data loaded from {path}")
        self.refresh_all_dropdowns(); self.refresh_tables()

    def export_csv(self):
        """
        Export students, instructors, and courses to CSV files in a chosen folder.

        :return: None
        :rtype: None
        """
        folder = QFileDialog.getExistingDirectory(self,"Choose folder to export CSV")
        if not folder: return
        with open(f"{folder}/students.csv","w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["student_id","name","age","email","courses"])
            for s in students: w.writerow([s.student_id,s.name,s.age,s._email, ",".join(c.course_id for c in s.registered_courses)])
        with open(f"{folder}/instructors.csv","w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["instructor_id","name","age","email","assigned_courses"])
            for i in instructors: w.writerow([i.instructor_id,i.name,i.age,i._email, ",".join(c.course_id for c in i.assigned_courses)])
        with open(f"{folder}/courses.csv","w",newline="",encoding="utf-8") as f:
            w=csv.writer(f); w.writerow(["course_id","course_name","instructor_id","enrolled_students"])
            for c in courses: w.writerow([c.course_id,c.course_name,c.instructor.instructor_id, ",".join(s.student_id for s in c.enrolled_students)])
        alert(self,"Exported",f"CSV files saved in:\n{folder}")


    def refresh_all_dropdowns(self):
        """
        Refresh the contents of student/course/instructor comboboxes.

        :return: None
        :rtype: None
        """
        self.reg_student.clear(); self.reg_student.addItems([f"{s.student_id} - {s.name}" for s in students])
        self.reg_course.clear();  self.reg_course.addItems([f"{c.course_id} - {c.course_name}" for c in courses])
        self.asg_instructor.clear(); self.asg_instructor.addItems([f"{i.instructor_id} - {i.name}" for i in instructors])
        self.asg_course.clear();     self.asg_course.addItems([f"{c.course_id} - {c.course_name}" for c in courses])

    def refresh_tables(self):
        """
        Refresh the students, instructors, and courses tables with current data.

        Applies a case-insensitive search filter on ID/name/email fields.

        :return: None
        :rtype: None
        """
        ft = self.search_line.text().lower().strip()
        self.stu_table.setRowCount(0)
        for s in students:
            row = [s.student_id, s.name, str(s.age), s._email, ", ".join(c.course_id for c in s.registered_courses)]
            if not ft or any(ft in x.lower() for x in row):
                r=self.stu_table.rowCount(); self.stu_table.insertRow(r)
                for j,v in enumerate(row): self.stu_table.setItem(r,j,QTableWidgetItem(v))
        self.ins_table.setRowCount(0)
        for i in instructors:
            row = [i.instructor_id, i.name, str(i.age), i._email, ", ".join(c.course_id for c in i.assigned_courses)]
            if not ft or any(ft in x.lower() for x in row):
                r=self.ins_table.rowCount(); self.ins_table.insertRow(r)
                for j,v in enumerate(row): self.ins_table.setItem(r,j,QTableWidgetItem(v))
        self.crs_table.setRowCount(0)
        for c in courses:
            row = [c.course_id, c.course_name, c.instructor.instructor_id if c.instructor else "", ", ".join(s.student_id for s in c.enrolled_students)]
            if not ft or any(ft in x.lower() for x in row):
                r=self.crs_table.rowCount(); self.crs_table.insertRow(r)
                for j,v in enumerate(row): self.crs_table.setItem(r,j,QTableWidgetItem(v))


    def load_student_into_form(self):
        """
        Load the selected student record from the table into the student form fields.

        :return: None
        :rtype: None
        """
        r = self.stu_table.currentRow(); 
        if r < 0: return
        self.stu_id.setText(self.stu_table.item(r,0).text())
        self.stu_name.setText(self.stu_table.item(r,1).text())
        self.stu_age.setText(self.stu_table.item(r,2).text())
        self.stu_email.setText(self.stu_table.item(r,3).text())

    def load_instructor_into_form(self):
        """
        Load the selected instructor record from the table into the instructor form fields.

        :return: None
        :rtype: None
        """
        r = self.ins_table.currentRow(); 
        if r < 0: return
        self.ins_id.setText(self.ins_table.item(r,0).text())
        self.ins_name.setText(self.ins_table.item(r,1).text())
        self.ins_age.setText(self.ins_table.item(r,2).text())
        self.ins_email.setText(self.ins_table.item(r,3).text())

    def load_course_into_form(self):
        """
        Load the selected course record from the table into the course form fields.

        :return: None
        :rtype: None
        """
        r = self.crs_table.currentRow(); 
        if r < 0: return
        self.crs_id.setText(self.crs_table.item(r,0).text())
        self.crs_name.setText(self.crs_table.item(r,1).text())
        self.crs_inst_id.setText(self.crs_table.item(r,2).text())


if __name__ == "__main__":
    """
    Application entry point. Ensures the database exists, starts the Qt app,
    and shows the main window.

    :return: None
    :rtype: None
    """
    init_db(DB_PATH)
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
