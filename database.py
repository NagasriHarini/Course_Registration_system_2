import pyodbc
from werkzeug.security import generate_password_hash, check_password_hash

connection_string = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=course_registration_system;"
    "Trusted_Connection=yes;"
)

def register_student(data):

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    hashed_password = generate_password_hash(data["password"])

    cursor.execute("""
        INSERT INTO Students
        (
            first_name,
            last_name,
            email,
            password,
            department,
            year_of_study,
            phone_number,
            section
        )
        OUTPUT INSERTED.student_id
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["first_name"],
        data["last_name"],
        data["email"],
        hashed_password,
        data["department"],
        data["year_of_study"],
        data["phone_number"],
        data["section"]
    ))

    student_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return student_id
def login_student(data):

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT student_id, password
        FROM Students
        WHERE student_id = ?
    """, (data["student_id"],))

    student = cursor.fetchone()

    cursor.close()
    conn.close()

    # Student ID does not exist
    if student is None:
        return False

    student_id = student[0]
    hashed_password = student[1]

    # Check entered password against hashed password
    if check_password_hash(hashed_password, data["password"]):
        return student_id

    return False
