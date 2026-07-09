import pyodbc

conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost\\SQLEXPRESS;"
    "DATABASE=course_registration_system;"
    "Trusted_Connection=yes;"
)

print("Connected successfully!")