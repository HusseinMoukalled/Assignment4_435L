import sqlite3
import shutil
from contextlib import closing


def get_conn(path="school.db"):
    """
    Create and return a connection to the SQLite database.

    :param path: Path to the SQLite database file. Defaults to ``school.db``.
    :type path: str
    :return: SQLite connection object.
    :rtype: sqlite3.Connection
    """
    return sqlite3.connect(path)


def init_db(path="school.db"):
    """
    Initialize the database by creating required tables if they do not exist.

    Tables created:
      - students
      - instructors
      - courses
      - enrollments

    :param path: Path to the SQLite database file. Defaults to ``school.db``.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        c = conn.cursor()
        c.execute("""CREATE TABLE IF NOT EXISTS students(
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS instructors(
            instructor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            email TEXT NOT NULL
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS courses(
            course_id TEXT PRIMARY KEY,
            course_name TEXT NOT NULL,
            instructor_id TEXT NOT NULL,
            FOREIGN KEY (instructor_id) REFERENCES instructors(instructor_id)
        )""")
        c.execute("""CREATE TABLE IF NOT EXISTS enrollments(
            student_id TEXT NOT NULL,
            course_id TEXT NOT NULL,
            PRIMARY KEY(student_id, course_id),
            FOREIGN KEY (student_id) REFERENCES students(student_id),
            FOREIGN KEY (course_id) REFERENCES courses(course_id)
        )""")
        conn.commit()


def db_add_student(student_id, name, age, email, path="school.db"):
    """
    Insert a new student into the students table.

    :param student_id: Unique identifier for the student.
    :type student_id: str
    :param name: Student's name.
    :type name: str
    :param age: Student's age.
    :type age: int
    :param email: Student's email address.
    :type email: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("INSERT INTO students(student_id,name,age,email) VALUES(?,?,?,?)",
                     (student_id, name, age, email))


def db_update_student(student_id, name, age, email, path="school.db"):
    """
    Update an existing student's details.

    :param student_id: ID of the student to update.
    :type student_id: str
    :param name: Updated student name.
    :type name: str
    :param age: Updated student age.
    :type age: int
    :param email: Updated student email.
    :type email: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("UPDATE students SET name=?, age=?, email=? WHERE student_id=?",
                     (name, age, email, student_id))


def db_delete_student(student_id, path="school.db"):
    """
    Delete a student and their enrollments from the database.

    :param student_id: ID of the student to delete.
    :type student_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("DELETE FROM enrollments WHERE student_id=?", (student_id,))
        conn.execute("DELETE FROM students WHERE student_id=?", (student_id,))


def db_add_instructor(instructor_id, name, age, email, path="school.db"):
    """
    Insert a new instructor into the instructors table.

    :param instructor_id: Unique identifier for the instructor.
    :type instructor_id: str
    :param name: Instructor's name.
    :type name: str
    :param age: Instructor's age.
    :type age: int
    :param email: Instructor's email address.
    :type email: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("INSERT INTO instructors(instructor_id,name,age,email) VALUES(?,?,?,?)",
                     (instructor_id, name, age, email))


def db_update_instructor(instructor_id, name, age, email, path="school.db"):
    """
    Update an existing instructor's details.

    :param instructor_id: ID of the instructor to update.
    :type instructor_id: str
    :param name: Updated instructor name.
    :type name: str
    :param age: Updated instructor age.
    :type age: int
    :param email: Updated instructor email.
    :type email: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("UPDATE instructors SET name=?, age=?, email=? WHERE instructor_id=?",
                     (name, age, email, instructor_id))


def db_delete_instructor(instructor_id, path="school.db"):
    """
    Delete an instructor from the database.

    :param instructor_id: ID of the instructor to delete.
    :type instructor_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("DELETE FROM instructors WHERE instructor_id=?", (instructor_id,))


def db_add_course(course_id, course_name, instructor_id, path="school.db"):
    """
    Insert a new course into the courses table.

    :param course_id: Unique identifier for the course.
    :type course_id: str
    :param course_name: Name of the course.
    :type course_name: str
    :param instructor_id: ID of the instructor assigned to the course.
    :type instructor_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("INSERT INTO courses(course_id,course_name,instructor_id) VALUES(?,?,?)",
                     (course_id, course_name, instructor_id))


def db_update_course(course_id, course_name, instructor_id, path="school.db"):
    """
    Update an existing course's details.

    :param course_id: ID of the course to update.
    :type course_id: str
    :param course_name: Updated course name.
    :type course_name: str
    :param instructor_id: Updated instructor ID assigned to the course.
    :type instructor_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("UPDATE courses SET course_name=?, instructor_id=? WHERE course_id=?",
                     (course_name, instructor_id, course_id))


def db_delete_course(course_id, path="school.db"):
    """
    Delete a course and its related enrollments.

    :param course_id: ID of the course to delete.
    :type course_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("DELETE FROM enrollments WHERE course_id=?", (course_id,))
        conn.execute("DELETE FROM courses WHERE course_id=?", (course_id,))


def db_enroll(student_id, course_id, path="school.db"):
    """
    Enroll a student in a course.

    :param student_id: ID of the student to enroll.
    :type student_id: str
    :param course_id: ID of the course to enroll the student in.
    :type course_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("INSERT OR IGNORE INTO enrollments(student_id, course_id) VALUES(?,?)",
                     (student_id, course_id))


def db_unenroll(student_id, course_id, path="school.db"):
    """
    Unenroll a student from a course.

    :param student_id: ID of the student to unenroll.
    :type student_id: str
    :param course_id: ID of the course from which to unenroll.
    :type course_id: str
    :param path: Path to the SQLite database file.
    :type path: str
    :return: None
    """
    with get_conn(path) as conn:
        conn.execute("DELETE FROM enrollments WHERE student_id=? AND course_id=?",
                     (student_id, course_id))


def db_fetch_all(path="school.db"):
    """
    Fetch all data from the database tables.

    Retrieves:
      - All students
      - All instructors
      - All courses
      - All enrollments

    :param path: Path to the SQLite database file.
    :type path: str
    :return: Dictionary containing lists of students, instructors, courses, and enrollments.
    :rtype: dict
    """
    with get_conn(path) as conn, closing(conn.cursor()) as c:
        c.execute("SELECT student_id,name,age,email FROM students")
        students = c.fetchall()
        c.execute("SELECT instructor_id,name,age,email FROM instructors")
        instructors = c.fetchall()
        c.execute("SELECT course_id,course_name,instructor_id FROM courses")
        courses = c.fetchall()
        c.execute("SELECT student_id,course_id FROM enrollments")
        enrollments = c.fetchall()
    return {
        "students": students,
        "instructors": instructors,
        "courses": courses,
        "enrollments": enrollments,
    }


def backup_db(src="school.db", dst="school_backup.db"):
    """
    Create a backup copy of the database.

    :param src: Source database file. Defaults to ``school.db``.
    :type src: str
    :param dst: Destination backup file. Defaults to ``school_backup.db``.
    :type dst: str
    :return: Path to the backup file.
    :rtype: str
    """
    shutil.copyfile(src, dst)
    return dst
