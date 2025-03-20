import pyodbc

def get_conn():
    connection_string = (
        'Driver={ODBC Driver 18 for SQL Server};'
        'Server=tcp:attendancemonitoring.database.windows.net,1433;'
        'Database=attendancemonitoring;'
        'Uid=cloudproj;'
        'Pwd=Goli@123;'
        'Encrypt=yes;'
        'TrustServerCertificate=no;'
        'Connection Timeout=30'
    )
    return pyodbc.connect(connection_string)

def create_tables():
    conn = get_conn()
    cursor = conn.cursor()

    # Create admins table
    cursor.execute("""
        CREATE TABLE admins (
            username VARCHAR(50) PRIMARY KEY,
            admin_name VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(15)
        )
    """)

    # Create teachers table
    cursor.execute("""
        CREATE TABLE teachers (
            username VARCHAR(50) PRIMARY KEY,
            teacher_name VARCHAR(50) NOT NULL,
            password VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            phone VARCHAR(15)
        )
    """)

    # Create students table
    cursor.execute("""
        CREATE TABLE students (
            student_id INT IDENTITY(1,1) PRIMARY KEY,
            student_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            class_sec VARCHAR(10) NOT NULL,
            phone VARCHAR(15)
        )
    """)

    # Create classes table
    cursor.execute("""
        CREATE TABLE classes (
            class_id INT IDENTITY(1,1) PRIMARY KEY,
            class_name VARCHAR(100) NOT NULL,
            teacher_username VARCHAR(50) NOT NULL,
            class_date DATE NOT NULL,
            class_sec VARCHAR(10) NOT NULL,
            FOREIGN KEY (teacher_username) REFERENCES teachers(username) ON DELETE CASCADE
        )
    """)

    # Create attendance table
    cursor.execute("""
        CREATE TABLE attendance (
            id INT IDENTITY(1,1) PRIMARY KEY,
            class_id INT NOT NULL,
            student_id INT NOT NULL,
            status VARCHAR(10) NOT NULL,
            FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE CASCADE,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
        )
    """)

    # Commit changes
    conn.commit()

    print("Tables created successfully.")

def insert_sample_data():
    conn = get_conn()
    cursor = conn.cursor()

    # Insert into admins table
    cursor.execute("""
        INSERT INTO admins (username, admin_name, password, email, phone)
        VALUES ('admin1', 'kittu', 'k', 'kittu@emaile.com', '1234567890')
    """)

    # Insert into teachers table
    cursor.execute("""
        INSERT INTO teachers (username, teacher_name, password, email, phone)
        VALUES
        ('valleti', 'mahi', 'v', 'mahi@gmail.com', '7894561230'),
        ('goli', 'surya', 'g', 'surya@gmail.com', '9183885580')
    """)

    # Insert into students table
    cursor.execute("""
        INSERT INTO students (student_name, email, class_sec, phone)
        VALUES
        ('surya', 'surya@gmail.com', 'AIE', '9515903559')
    """)

    # Insert into classes table
    cursor.execute("""
        INSERT INTO classes (class_name, teacher_username, class_date, class_sec)
        VALUES
        ('cloud computing', 'goli', '2024-10-22', 'AIE'),
        ('java', 'goli', '2024-10-23', 'AIE'),
        ('ml', 'valleti', '2024-11-04', 'AIE'),
        ('mathematics', 'valleti', '2024-11-03', 'AIE'),
        ('java', 'valleti', '2024-11-04', 'AIE')
    """)

#     # Insert into attendance table
#     cursor.execute("""
#         INSERT INTO attendance (class_id, student_id, status)
# VALUES (1, 1, 'present');

#     """)

    # Commit changes
    conn.commit()

    print("Sample data inserted successfully.")

def main():
    # Create tables and insert data
    # create_tables()
    insert_sample_data()

if __name__ == "__main__":
    main()
