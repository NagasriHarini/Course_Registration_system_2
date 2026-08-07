import pyodbc
from werkzeug.security import generate_password_hash

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
        (first_name, last_name, email,
         password, department, year_of_study, phone_number,section)
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

    conn.commit()
    cursor.close()
    conn.close()