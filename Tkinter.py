#On my honor I have neither given nor received unauthorized aid on this assignment. I used AI tools to research concepts, understand the code and get templates.

import json
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

class Person:
    def __init__(self, name: str, age: int, email: str):

        if not isinstance(age,int) or age<0:
            raise ValueError("Age must be a positive integer")
        if not isinstance(email, str) or "@" not in email or "." not in email.split('@')[-1]: #email.split('@')[-1] returns a list where the part after the @ is the last entry (at idx -1) and we check for a '.' in it
            raise ValueError("Email must be a string of valid format: name@example.com")
        self.name=name
        self.age=age
        self._email=email  #the single _ in python is to indicate that the attribute is not to be used outside the class (dosn't actually enfore it, it's more of a convention)

    def introduce(self):
        print(f"My name is {self.name} and I am {self.age} years old.")
        
class Student(Person): #Subclass basically means it inherits from Person class, so uses all its attributes + its own
    def __init__(self, name: str, age: int, email: str, student_id: str): #I didn't include registered_courses as an attribute here because It should start off as an empty list for all students, 
        #therefor rather than forcing user to define an instance as: Student(Hussein, 21, ham69, 202306, [] or some course name) the user can just define an instance as: Student(Hussein, 21, ham69, 202306)
        super().__init__(name, age, email) #used to inherit the attributes from parent Person class

        self.student_id=student_id #new attribute for student class so we define it
        self.registered_courses=[] #now we define the attribute registered_courses as an empty list. Again the entire point is not to force users to enter a course name when creating the instance 

    def register_course(self, course):
        if not isinstance(course, Course):  #This ensures the constraints listed in the class definition are met: the student must register to a course that is an instance of the course Class
            raise TypeError("This course is not recognized")
        self.registered_courses.append(course)  #whenever this method is called, the course is added to the registered_courses list

class Instructor(Person):
    def __init__(self, name: str, age: int, email: str, instructor_id: str): #As per the reasonning for the Student subclass, we don't include assigned_courses as an attribute
        super().__init__(name, age, email)
        self.instructor_id=instructor_id
        self.assigned_courses=[]

    def assign_course(self, course):
        if not isinstance(course, Course):
            raise TypeError("This course is not recognized")
        self.assigned_courses.append(course)

class Course:
    def __init__(self, course_id: str, course_name: str, instructor):
        if not isinstance(instructor, Instructor):
            raise TypeError("This instructor is not recognized")
        self.course_id=course_id
        self.course_name=course_name
        self.instructor=instructor
        self.enrolled_students=[]

    def add_student(self, student):
        if not isinstance(student, Student):
            raise TypeError("This student is not recognized")
        self.enrolled_students.append(student)



def serialization_json(students, instructors, courses): #We will now work on saving and loading to the classes created using JSON
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
    data=serialization_json(students, instructors, courses)
    f=open(filename,"w")
    json.dump(data,f)
    print("Data successfully saved to", filename)
    f.close()

def load_from_file(filename):
    f=open(filename, "r")
    data=json.load(f)
    print("Data loaded successfully from", filename)
    return data
    f.close()


from db_helper import (
    init_db, db_fetch_all, backup_db,
    db_add_student, db_update_student, db_delete_student,
    db_add_instructor, db_update_instructor, db_delete_instructor,
    db_add_course, db_update_course, db_delete_course,
    db_enroll
)
DB_PATH = "school.db"
init_db(DB_PATH)

def load_from_database():
    data = db_fetch_all(DB_PATH)
    students.clear(); instructors.clear(); courses.clear()
    for iid, name, age, email in data["instructors"]:
        instructors.append(Instructor(name, int(age), email, iid))

    for sid, name, age, email in data["students"]:
        students.append(Student(name, int(age), email, sid))

    def _find_instr(iid): return next((x for x in instructors if x.instructor_id == iid), None)
    for cid, cname, iid in data["courses"]:
        ins = _find_instr(iid)
        if not ins: continue
        c = Course(cid, cname, ins)
        courses.append(c); ins.assign_course(c)
    
    def _find_stu(sid): return next((x for x in students if x.student_id == sid), None)
    def _find_crs(cid): return next((x for x in courses if x.course_id == cid), None)
    for sid, cid in data["enrollments"]:
        s = _find_stu(sid); c = _find_crs(cid)
        if s and c and s not in c.enrolled_students:
            c.add_student(s); s.register_course(c)

    refresh_registration_dropdowns()
    refresh_assignment_dropdowns()
    refresh_tables()
    messagebox.showinfo("DB", "Loaded from SQLite database.")



import tkinter as tk
from tkinter import ttk, messagebox

root = tk.Tk()
root.title("School Management System")
root.geometry("900x650") 


outer = tk.Frame(root)
outer.pack(fill="both", expand=True)

canvas = tk.Canvas(outer, highlightthickness=0)
vbar = tk.Scrollbar(outer, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vbar.set)

vbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

content = tk.Frame(canvas)
canvas.create_window((0, 0), window=content, anchor="nw")

def _on_frame_config(_):
    canvas.configure(scrollregion=canvas.bbox("all"))
content.bind("<Configure>", _on_frame_config)


def _on_mousewheel(event):
    if event.delta: 
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
def _on_linux_up(event): canvas.yview_scroll(-3, "units")
def _on_linux_down(event): canvas.yview_scroll(3, "units")
canvas.bind_all("<MouseWheel>", _on_mousewheel)
canvas.bind_all("<Button-4>", _on_linux_up)
canvas.bind_all("<Button-5>", _on_linux_down)

students = []
instructors = []
courses = []

def find_student(student_id):
    for s in students:
        if s.student_id == student_id:
            return s
    return None

def find_instructor(instructor_id):
    for i in instructors:
        if i.instructor_id == instructor_id:
            return i
    return None

def find_course(course_id):
    for c in courses:
        if c.course_id == course_id:
            return c
    return None


student_frame = tk.LabelFrame(content, text="Add new Student", padx=9, pady=9)
student_frame.pack(fill="x", padx=8, pady=6)

tk.Label(student_frame, text="Student Name").grid(row=0, column=0, sticky="w")
tk.Label(student_frame, text="Student Age").grid(row=1, column=0, sticky="w")
tk.Label(student_frame, text="Student Email").grid(row=2, column=0, sticky="w")
tk.Label(student_frame, text="Student ID").grid(row=3, column=0, sticky="w")

student_name  = tk.Entry(student_frame, width=30)
student_age   = tk.Entry(student_frame, width=30)
student_email = tk.Entry(student_frame, width=30)
student_id    = tk.Entry(student_frame, width=30)

student_name.grid(row=0, column=1)
student_age.grid(row=1, column=1)
student_email.grid(row=2, column=1)
student_id.grid(row=3, column=1)

def add_student():
    try:
        name  = student_name.get().strip()
        age   = int(student_age.get().strip())
        email = student_email.get().strip()
        sid   = student_id.get().strip()

        if not name or not sid:
            messagebox.showerror("Error", "Name and Student ID are required")
            return
        if find_student(sid):
            messagebox.showerror("Error", "Student ID already exists")
            return

        s = Student(name, age, email, sid)
        students.append(s)
        db_add_student(sid, name, age, email, DB_PATH)  # NEW
        messagebox.showinfo("OK", f"Student '{name}' added")
        refresh_registration_dropdowns()
        refresh_tables()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def update_student_record():
    sid = student_id.get().strip()
    s = find_student(sid)
    if not s:
        messagebox.showerror("Error", "Student not found by ID")
        return
    try:
        s.name = student_name.get().strip()
        s.age = int(student_age.get().strip())
        s._email = student_email.get().strip()
        db_update_student(sid, s.name, s.age, s._email, DB_PATH)  # NEW
        messagebox.showinfo("OK", "Student updated")
        refresh_tables()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def delete_student_by_id():
    sid = student_id.get().strip()
    s = find_student(sid)
    if not s:
        messagebox.showerror("Error", "Student not found by ID")
        return
    for c in courses:
        if s in c.enrolled_students:
            c.enrolled_students.remove(s)
    students.remove(s)
    messagebox.showinfo("OK", f"Deleted student {sid}")
    refresh_registration_dropdowns()
    refresh_tables()

tk.Button(student_frame, text="Add Student", command=add_student).grid(row=4, column=0, pady=7, sticky="w")
tk.Button(student_frame, text="Update Student (by ID)", command=update_student_record).grid(row=4, column=1, pady=7, sticky="e")
tk.Button(student_frame, text="Delete Student (by ID)", command=delete_student_by_id).grid(row=5, column=0, columnspan=2, pady=4)


instructor_frame = tk.LabelFrame(content, text="Add new Instructor", padx=9, pady=9)
instructor_frame.pack(fill="x", padx=8, pady=6)

tk.Label(instructor_frame, text="Instructor Name").grid(row=0, column=0, sticky="w")
tk.Label(instructor_frame, text="Instructor Age").grid(row=1, column=0, sticky="w")
tk.Label(instructor_frame, text="Instructor Email").grid(row=2, column=0, sticky="w")
tk.Label(instructor_frame, text="Instructor ID").grid(row=3, column=0, sticky="w")

instructor_name  = tk.Entry(instructor_frame, width=30)
instructor_age   = tk.Entry(instructor_frame, width=30)
instructor_email = tk.Entry(instructor_frame, width=30)
instructor_id    = tk.Entry(instructor_frame, width=30)

instructor_name.grid(row=0, column=1)
instructor_age.grid(row=1, column=1)
instructor_email.grid(row=2, column=1)
instructor_id.grid(row=3, column=1)

def add_instructor():
    try:
        name  = instructor_name.get().strip()
        age   = int(instructor_age.get().strip())
        email = instructor_email.get().strip()
        iid   = instructor_id.get().strip()

        if not name or not iid:
            messagebox.showerror("Error", "Name and Instructor ID are required")
            return
        if find_instructor(iid):
            messagebox.showerror("Error", "Instructor ID already exists")
            return

        i = Instructor(name, age, email, iid)
        instructors.append(i)
        db_add_instructor(iid, name, age, email, DB_PATH)  # NEW
        messagebox.showinfo("OK", f"Instructor '{name}' added")
        refresh_assignment_dropdowns()
        refresh_tables()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def update_instructor_record():
    iid = instructor_id.get().strip()
    ins = find_instructor(iid)
    if not ins:
        messagebox.showerror("Error", "Instructor not found by ID")
        return
    try:
        ins.name = instructor_name.get().strip()
        ins.age = int(instructor_age.get().strip())
        ins._email = instructor_email.get().strip()
        db_update_instructor(iid, ins.name, ins.age, ins._email, DB_PATH)  # NEW
        messagebox.showinfo("OK", "Instructor updated")
        refresh_tables()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


def delete_instructor_by_id():
    iid = instructor_id.get().strip()
    ins = find_instructor(iid)
    if not ins:
        messagebox.showerror("Error", "Instructor not found by ID")
        return
    if ins.assigned_courses:
        messagebox.showerror("Error", "Cannot delete: instructor has assigned courses. Reassign first.")
        return
    instructors.remove(ins)
    messagebox.showinfo("OK", f"Deleted instructor {iid}")
    refresh_assignment_dropdowns()
    refresh_tables()

tk.Button(instructor_frame, text="Add Instructor", command=add_instructor).grid(row=4, column=0, pady=7, sticky="w")
tk.Button(instructor_frame, text="Update Instructor (by ID)", command=update_instructor_record).grid(row=4, column=1, pady=7, sticky="e")
tk.Button(instructor_frame, text="Delete Instructor (by ID)", command=delete_instructor_by_id).grid(row=5, column=0, columnspan=2, pady=4)


course_frame = tk.LabelFrame(content, text="Add new Course", padx=9, pady=9)
course_frame.pack(fill="x", padx=8, pady=6)

tk.Label(course_frame, text="Course ID").grid(row=0, column=0, sticky="w")
tk.Label(course_frame, text="Course Name").grid(row=1, column=0, sticky="w")
tk.Label(course_frame, text="Instructor ID (must be registered)").grid(row=2, column=0, sticky="w")

course_id   = tk.Entry(course_frame, width=30)
course_name = tk.Entry(course_frame, width=30)
course_inst = tk.Entry(course_frame, width=30)

course_id.grid(row=0, column=1)
course_name.grid(row=1, column=1)
course_inst.grid(row=2, column=1)

def add_course():
    cid = course_id.get().strip()
    cname = course_name.get().strip()
    iid = course_inst.get().strip()

    if not cid or not cname or not iid:
        messagebox.showerror("Error", "Course ID, Name, and Instructor ID are required")
        return
    if find_course(cid):
        messagebox.showerror("Error", "Course ID already exists")
        return

    inst = find_instructor(iid)
    if not inst:
        messagebox.showerror("Error", "Instructor not found")
        return

    try:
        c = Course(cid, cname, inst)
        courses.append(c)
        inst.assign_course(c)
        db_add_course(cid, cname, iid, DB_PATH)  # NEW
        messagebox.showinfo("OK", f"Course '{cname}' added")
        refresh_registration_dropdowns()
        refresh_assignment_dropdowns()
        refresh_tables()
    except TypeError as e:
        messagebox.showerror("Error", str(e))


def update_course_record():
    cid = course_id.get().strip()
    crs = find_course(cid)
    if not crs:
        messagebox.showerror("Error", "Course not found by ID")
        return
    cname = course_name.get().strip()
    iid = course_inst.get().strip()
    inst = find_instructor(iid) if iid else None
    if not cname:
        messagebox.showerror("Error", "Course name required"); return
    if not inst:
        messagebox.showerror("Error", "Instructor not found by ID"); return

    if crs.instructor != inst:
        if crs.instructor and crs in crs.instructor.assigned_courses:
            crs.instructor.assigned_courses.remove(crs)
        inst.assign_course(crs)
        crs.instructor = inst

    crs.course_name = cname
    db_update_course(cid, cname, iid, DB_PATH)  # NEW
    messagebox.showinfo("OK", "Course updated")
    refresh_assignment_dropdowns()
    refresh_tables()



def delete_course_by_id():
    cid = course_id.get().strip()
    crs = find_course(cid)
    if not crs:
        messagebox.showerror("Error", "Course not found by ID")
        return
    if crs.instructor and crs in crs.instructor.assigned_courses:
        crs.instructor.assigned_courses.remove(crs)
    for s in students:
        if crs in s.registered_courses:
            s.registered_courses.remove(crs)
    courses.remove(crs)
    messagebox.showinfo("OK", f"Deleted course {cid}")
    refresh_registration_dropdowns()
    refresh_assignment_dropdowns()
    refresh_tables()

tk.Button(course_frame, text="Add Course", command=add_course).grid(row=3, column=0, pady=7, sticky="w")
tk.Button(course_frame, text="Update Course (by ID)", command=update_course_record).grid(row=3, column=1, pady=7, sticky="e")
tk.Button(course_frame, text="Delete Course (by ID)", command=delete_course_by_id).grid(row=4, column=0, columnspan=2, pady=4)


reg_frame = tk.LabelFrame(content, text="Register Student in Course", padx=9, pady=9)
reg_frame.pack(fill="x", padx=8, pady=6)

selected_student = tk.StringVar(value="-- select student --")
selected_course  = tk.StringVar(value="-- select course --")

def _stu_label(s): return f"{s.student_id} - {s.name}"
def _crs_label(c): return f"{c.course_id} - {c.course_name}"

tk.Label(reg_frame, text="Student").grid(row=0, column=0, sticky="w")
student_menu = tk.OptionMenu(reg_frame, selected_student, "-- select student --")
student_menu.config(width=32)
student_menu.grid(row=0, column=1, sticky="w")

tk.Label(reg_frame, text="Course").grid(row=1, column=0, sticky="w")
course_menu = tk.OptionMenu(reg_frame, selected_course, "-- select course --")
course_menu.config(width=32)
course_menu.grid(row=1, column=1, sticky="w")

def refresh_registration_dropdowns():
    menu = student_menu["menu"]
    menu.delete(0, "end")
    if students:
        for s in students:
            lbl = _stu_label(s)
            menu.add_command(label=lbl, command=tk._setit(selected_student, lbl))
        if selected_student.get().startswith("--"):
            selected_student.set(_stu_label(students[0]))
    else:
        selected_student.set("-- select student --")

    menu = course_menu["menu"]
    menu.delete(0, "end")
    if courses:
        for c in courses:
            lbl = _crs_label(c)
            menu.add_command(label=lbl, command=tk._setit(selected_course, lbl))
        if selected_course.get().startswith("--"):
            selected_course.set(_crs_label(courses[0]))
    else:
        selected_course.set("-- select course --")

def register_student_in_course():
    s_lbl = selected_student.get()
    c_lbl = selected_course.get()
    if s_lbl.startswith("--") or c_lbl.startswith("--"):
        messagebox.showerror("Error", "Please select both a student and a course")
        return
    sid = s_lbl.split(" - ", 1)[0]
    cid = c_lbl.split(" - ", 1)[0]
    s = find_student(sid)
    c = find_course(cid)
    if not s or not c:
        messagebox.showerror("Error", "Could not find selected student/course")
        return
    if s in c.enrolled_students:
        messagebox.showinfo("Info", f"{s.name} is already enrolled in {c.course_name}")
        return
    try:
        c.add_student(s)
        s.register_course(c)
        db_enroll(sid, cid, DB_PATH)  # NEW
        messagebox.showinfo("OK", f"Enrolled {s.name} in {c.course_name}")
        refresh_tables()
    except TypeError as e:
        messagebox.showerror("Error", str(e))


tk.Button(reg_frame, text="Register", command=register_student_in_course).grid(row=2, column=0, columnspan=2, pady=7)


assign_frame = tk.LabelFrame(content, text="Assign Instructor to Course", padx=9, pady=9)
assign_frame.pack(fill="x", padx=8, pady=6)

selected_instructor = tk.StringVar(value="-- select instructor --")
selected_course_for_inst = tk.StringVar(value="-- select course --")

def _inst_label(i): return f"{i.instructor_id} - {i.name}"
def _course_label(c): return f"{c.course_id} - {c.course_name}"

tk.Label(assign_frame, text="Instructor").grid(row=0, column=0, sticky="w")
instructor_menu = tk.OptionMenu(assign_frame, selected_instructor, "-- select instructor --")
instructor_menu.config(width=32)
instructor_menu.grid(row=0, column=1, sticky="w")

tk.Label(assign_frame, text="Course").grid(row=1, column=0, sticky="w")
course_menu_inst = tk.OptionMenu(assign_frame, selected_course_for_inst, "-- select course --")
course_menu_inst.config(width=32)
course_menu_inst.grid(row=1, column=1, sticky="w")

def refresh_assignment_dropdowns():
    menu = instructor_menu["menu"]
    menu.delete(0, "end")
    if instructors:
        for i in instructors:
            lbl = _inst_label(i)
            menu.add_command(label=lbl, command=tk._setit(selected_instructor, lbl))
        if selected_instructor.get().startswith("--"):
            selected_instructor.set(_inst_label(instructors[0]))
    else:
        selected_instructor.set("-- select instructor --")

    menu = course_menu_inst["menu"]
    menu.delete(0, "end")
    if courses:
        for c in courses:
            lbl = _course_label(c)
            menu.add_command(label=lbl, command=tk._setit(selected_course_for_inst, lbl))
        if selected_course_for_inst.get().startswith("--"):
            selected_course_for_inst.set(_course_label(courses[0]))
    else:
        selected_course_for_inst.set("-- select course --")

def assign_instructor_to_course():
    i_lbl = selected_instructor.get()
    c_lbl = selected_course_for_inst.get()

    if i_lbl.startswith("--") or c_lbl.startswith("--"):
        messagebox.showerror("Error", "Please select both an instructor and a course")
        return

    iid = i_lbl.split(" - ", 1)[0]
    cid = c_lbl.split(" - ", 1)[0]

    instr = find_instructor(iid)
    crs = find_course(cid)
    if not instr or not crs:
        messagebox.showerror("Error", "Could not find the selected instructor/course")
        return

    if crs in instr.assigned_courses:
        messagebox.showinfo("Info", f"{instr.name} is already assigned to {crs.course_name}")
        return

    try:
        instr.assign_course(crs)
        crs.instructor = instr
        messagebox.showinfo("OK", f"Assigned {instr.name} to {crs.course_name}")
        refresh_assignment_dropdowns()
        refresh_tables()
    except TypeError as e:
        messagebox.showerror("Error", str(e))

tk.Button(assign_frame, text="Assign", command=assign_instructor_to_course).grid(row=2, column=0, columnspan=2, pady=7)

def save_and_notify():
    save_to_file("school_data.json", students, instructors, courses)
    messagebox.showinfo("Saved", "Data saved successfully!")

def load_and_restore():
    try:
        data = load_from_file("school_data.json")
    except FileNotFoundError:
        messagebox.showerror("Error", "school_data.json not found")
        return

    students.clear(); instructors.clear(); courses.clear()

    for i in data.get("instructors", []):
        ins = Instructor(i["name"], i["age"], i["email"], i["instructor_id"])
        instructors.append(ins)

    for s in data.get("students", []):
        stu = Student(s["name"], s["age"], s["email"], s["student_id"])
        students.append(stu)

    def _find_instr(iid):
        return next((x for x in instructors if x.instructor_id == iid), None)

    for c in data.get("courses", []):
        ins = _find_instr(c["instructor_id"])
        if not ins:
            continue
        crs = Course(c["course_id"], c["course_name"], ins)
        courses.append(crs)
        ins.assign_course(crs)

    def _find_stu(sid):
        return next((x for x in students if x.student_id == sid), None)

    for c in data.get("courses", []):
        crs = next((x for x in courses if x.course_id == c["course_id"]), None)
        if not crs:
            continue
        for sid in c.get("enrolled_students", []):
            stu = _find_stu(sid)
            if stu:
                try:
                    crs.add_student(stu)
                    if crs not in stu.registered_courses:
                        stu.register_course(crs)
                except TypeError:
                    pass

    messagebox.showinfo("Loaded", "Data loaded successfully")
    refresh_registration_dropdowns()
    refresh_assignment_dropdowns()
    refresh_tables()

btns_row = tk.Frame(content)
btns_row.pack(fill="x", padx=8, pady=(0,6))
tk.Button(btns_row, text="Save All Data", command=save_and_notify).pack(side="left", padx=4)
tk.Button(btns_row, text="Load Data", command=load_and_restore).pack(side="left", padx=4)

tk.Button(btns_row, text="Load from DB", command=load_from_database).pack(side="left", padx=4)

def do_backup():
    dst = backup_db(DB_PATH, "school_backup.db")
    messagebox.showinfo("Backup", f"Database copied to {dst}")

tk.Button(btns_row, text="Backup DB", command=do_backup).pack(side="left", padx=4)


search_frame = tk.Frame(content)
search_frame.pack(fill="x", padx=8, pady=(0,6))
tk.Label(search_frame, text="Search (name / ID / course):").pack(side="left")
search_entry = tk.Entry(search_frame, width=40)
search_entry.pack(side="left", padx=6)

def do_search():
    refresh_tables(search_entry.get())

tk.Button(search_frame, text="Search", command=do_search).pack(side="left", padx=4)
tk.Button(search_frame, text="Clear",
          command=lambda:(search_entry.delete(0,"end"), refresh_tables())).pack(side="left")

tables_frame = tk.LabelFrame(content, text="All Records", padx=9, pady=9)
tables_frame.pack(fill="both", expand=True, padx=8, pady=6)


stu_cols = ("student_id", "name", "age", "email", "courses")
students_tree = ttk.Treeview(tables_frame, columns=stu_cols, show="headings", height=6)
for c in stu_cols:
    students_tree.heading(c, text=c.title().replace("_", " "))
    students_tree.column(c, width=140 if c!="courses" else 220, anchor="w")
students_tree.grid(row=0, column=0, sticky="nsew", padx=(0,6))


inst_cols = ("instructor_id", "name", "age", "email", "assigned")
instructors_tree = ttk.Treeview(tables_frame, columns=inst_cols, show="headings", height=6)
for c in inst_cols:
    instructors_tree.heading(c, text=c.title().replace("_", " "))
    instructors_tree.column(c, width=140 if c!="assigned" else 220, anchor="w")
instructors_tree.grid(row=0, column=1, sticky="nsew", padx=(0,6))


crs_cols = ("course_id", "course_name", "instructor_id", "enrolled")
courses_tree = ttk.Treeview(tables_frame, columns=crs_cols, show="headings", height=6)
for c in crs_cols:
    courses_tree.heading(c, text=c.title().replace("_", " "))
    courses_tree.column(c, width=160 if c!="enrolled" else 240, anchor="w")
courses_tree.grid(row=0, column=2, sticky="nsew")

tables_frame.grid_columnconfigure(0, weight=1)
tables_frame.grid_columnconfigure(1, weight=1)
tables_frame.grid_columnconfigure(2, weight=1)
tables_frame.grid_rowconfigure(0, weight=1)

def refresh_tables(filter_text=""):
    ft = filter_text.lower().strip()


    for i in students_tree.get_children(): students_tree.delete(i)
    for s in students:
        courses_str = ", ".join([c.course_id for c in s.registered_courses])
        row = (s.student_id, s.name, s.age, s._email, courses_str)
        if not ft or any(ft in str(x).lower() for x in row):
            students_tree.insert("", "end", values=row)


    for i in instructors_tree.get_children(): instructors_tree.delete(i)
    for ins in instructors:
        assigned_str = ", ".join([c.course_id for c in ins.assigned_courses])
        row = (ins.instructor_id, ins.name, ins.age, ins._email, assigned_str)
        if not ft or any(ft in str(x).lower() for x in row):
            instructors_tree.insert("", "end", values=row)


    for i in courses_tree.get_children(): courses_tree.delete(i)
    for c in courses:
        instr_id = c.instructor.instructor_id if c.instructor else ""
        enrolled_str = ", ".join([s.student_id for s in c.enrolled_students])
        row = (c.course_id, c.course_name, instr_id, enrolled_str)
        if not ft or any(ft in str(x).lower() for x in row):
            courses_tree.insert("", "end", values=row)


def on_student_select(event):
    sel = students_tree.selection()
    if not sel: return
    vals = students_tree.item(sel[0], "values")
    sid, name, age, email = vals[0], vals[1], vals[2], vals[3]
    student_id.delete(0,"end"); student_id.insert(0, sid)
    student_name.delete(0,"end"); student_name.insert(0, name)
    student_age.delete(0,"end"); student_age.insert(0, str(age))
    student_email.delete(0,"end"); student_email.insert(0, email)

def on_instructor_select(event):
    sel = instructors_tree.selection()
    if not sel: return
    vals = instructors_tree.item(sel[0], "values")
    iid, name, age, email = vals[0], vals[1], vals[2], vals[3]
    instructor_id.delete(0,"end"); instructor_id.insert(0, iid)
    instructor_name.delete(0,"end"); instructor_name.insert(0, name)
    instructor_age.delete(0,"end"); instructor_age.insert(0, str(age))
    instructor_email.delete(0,"end"); instructor_email.insert(0, email)

def on_course_select(event):
    sel = courses_tree.selection()
    if not sel: return
    vals = courses_tree.item(sel[0], "values")
    cid, cname, iid = vals[0], vals[1], vals[2]
    course_id.delete(0,"end"); course_id.insert(0, cid)
    course_name.delete(0,"end"); course_name.insert(0, cname)
    course_inst.delete(0,"end"); course_inst.insert(0, iid)

students_tree.bind("<<TreeviewSelect>>", on_student_select)
instructors_tree.bind("<<TreeviewSelect>>", on_instructor_select)
courses_tree.bind("<<TreeviewSelect>>", on_course_select)

actions_row = tk.Frame(content)
actions_row.pack(fill="x", padx=8, pady=(0,6))
tk.Button(actions_row, text="Update Student", command=update_student_record).pack(side="left", padx=4)
tk.Button(actions_row, text="Update Instructor", command=update_instructor_record).pack(side="left", padx=4)
tk.Button(actions_row, text="Update Course", command=update_course_record).pack(side="left", padx=4)


def delete_selected_student():
    sel = students_tree.selection()
    if not sel: return
    sid = students_tree.item(sel[0], "values")[0]
    s = find_student(sid)
    if not s: return
    for c in courses:
        if s in c.enrolled_students:
            c.enrolled_students.remove(s)
    students.remove(s)
    db_delete_student(sid, DB_PATH) 
    messagebox.showinfo("OK", f"Deleted student {sid}")
    refresh_registration_dropdowns(); refresh_tables()

def delete_selected_instructor():
    sel = instructors_tree.selection()
    if not sel: return
    iid = instructors_tree.item(sel[0], "values")[0]
    ins = find_instructor(iid)
    if not ins: return
    if ins.assigned_courses:
        messagebox.showerror("Error", "Cannot delete: instructor has assigned courses. Reassign first.")
        return
    instructors.remove(ins)
    db_delete_instructor(iid, DB_PATH)  
    messagebox.showinfo("OK", f"Deleted instructor {iid}")
    refresh_assignment_dropdowns(); refresh_tables()


def delete_selected_course():
    sel = courses_tree.selection()
    if not sel: return
    cid = courses_tree.item(sel[0], "values")[0]
    crs = find_course(cid)
    if not crs: return
    if crs.instructor and crs in crs.instructor.assigned_courses:
        crs.instructor.assigned_courses.remove(crs)
    for s in students:
        if crs in s.registered_courses:
            s.registered_courses.remove(crs)
    courses.remove(crs)
    messagebox.showinfo("OK", f"Deleted course {cid}")
    refresh_registration_dropdowns(); refresh_assignment_dropdowns(); refresh_tables()

del_row = tk.Frame(content)
del_row.pack(fill="x", padx=8, pady=(0,10))
tk.Button(del_row, text="Delete Selected Student", command=delete_selected_student).pack(side="left", padx=4)
tk.Button(del_row, text="Delete Selected Instructor", command=delete_selected_instructor).pack(side="left", padx=4)
tk.Button(del_row, text="Delete Selected Course", command=delete_selected_course).pack(side="left", padx=4)

# Initial fills
refresh_registration_dropdowns()
refresh_assignment_dropdowns()
refresh_tables()

root.mainloop()
