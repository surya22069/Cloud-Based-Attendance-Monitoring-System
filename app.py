from flask import Flask, render_template, request, redirect, session, Response, json, make_response
import psycopg2
from psycopg2 import sql
import pyodbc

app = Flask(__name__)
import os
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'default_secret_key')




# Function to create a database if it doesn't exist
import psycopg2
from psycopg2 import sql



import pyodbc

def db():
        connection_string = (
            'Driver={ODBC Driver 18 for SQL Server};'
            'Server=tcp:attendancemonitoring.database.windows.net,1433;'
            'Database=attendancemonitoring;'
            'Uid=cloudproj;'
            'Pwd=Goli@123;'
            'Encrypt=yes;'
            'TrustServerCertificate=no;'
            'Connection Timeout=30;'
        )
        connection = pyodbc.connect(connection_string)
        print("Database connection successful.")
        return connection




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        connection = db()
        if connection is None:
            error_message = "Failed to connect to the database. Please try again later."
            return render_template('login.html', error=error_message)

        try:
            # Using a context manager to define the cursor
            with connection.cursor() as cur:
                if role == 'teacher':
                    cur.execute("SELECT * FROM teachers WHERE username = ? AND password = ?", (username, password))
                    user = cur.fetchone()
                    if user:
                        session['loggedin'] = True
                        session['username'] = user[0]
                        session['role'] = 'teacher'
                        return redirect('/teacher/dashboard')
                    else:
                        error = 'Invalid login credentials.'
                        return render_template('login.html', error=error)

                elif role == 'admin':
                    cur.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, password))
                    user = cur.fetchone()
                    if user:
                        session['loggedin'] = True
                        session['username'] = user[0]
                        session['role'] = 'admin'
                        return redirect('/admin/admin_dashboard')
                    else:
                        error = 'Invalid login credentials.'
                        return render_template('login.html', error=error)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('login.html', error=error_message)

        finally:
            # Ensure the connection is closed
            connection.close()

    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
        phone = request.form['phone']

        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            cur.execute("SELECT username FROM teachers WHERE username = ?", (username,))
            existing_user = cur.fetchone()

            if existing_user:
                error_message = "Username already exists. Please choose a different one."
                return render_template('teacher_registration.html', error=error_message)

            cur.execute("INSERT INTO teachers (teacher_name, username, password, email, phone) VALUES (?, ?, ?, ?, ?)",
                        (name, username, password, email, phone))
            connection.commit()
            return render_template('teacher_registration.html', message="Teacher successfully registered.")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('teacher_registration.html', error=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return render_template('teacher_registration.html')




@app.route('/student_register', methods=['GET', 'POST'])
def student_register():
    if request.method == "POST":
        student_id = request.form['student_id']
        name = request.form['name']
        class_sec = request.form['class_sec']
        email = request.form['email']
        phone = request.form['phone']

        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            cur.execute("SELECT student_id FROM students WHERE student_id = ?", (student_id,))
            existing_user = cur.fetchone()

            if existing_user:
                error_message = "Student ID already exists."
                return render_template('student_registration.html', error=error_message)

            cur.execute("INSERT INTO students (student_id, student_name, class_sec, email, phone) VALUES (?, ?, ?, ?, ?)",
                        (student_id, name, class_sec, email, phone))
            connection.commit()
            return render_template('student_registration.html', message="Student successfully registered.")

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('student_registration.html', error=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return render_template('student_registration.html')




@app.route('/get_student', methods=['POST', 'GET'])
def get_student():
    if request.method == 'POST':
        student_id = request.form['student_id']

        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()
            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cur.fetchone()

            if student:
                message = "Fetched student details."
                return render_template('update_student.html', student=student, msg=message)
            else:
                error = "Invalid Student ID."
                return render_template('update_student.html', err=error)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('update_student.html', err=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return render_template('update_student.html')



@app.route('/update_student', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        new_name = request.form['new_name']
        new_email = request.form['new_email']
        new_phone = request.form['new_phone']

        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            cur.execute("SELECT * FROM students WHERE student_id = ?", (student_id,))
            student = cur.fetchone()

            if student:
                cur.execute("UPDATE students SET student_name = ?, email = ?, phone = ? WHERE student_id = ?",
                            (new_name, new_email, new_phone, student_id))
                connection.commit()
                message = f"Student ID {student_id} details have been successfully updated."
                return render_template('update_student.html', student=student, message=message)
            else:
                error = "Invalid Student ID."
                return render_template('update_student.html', error=error)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('update_student.html', error=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return render_template('update_student.html')



@app.route('/teacher/dashboard')
def teacher_dashboard():
    if 'loggedin' in session and session['role'] == 'teacher':
        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            cur.execute("SELECT * FROM classes WHERE teacher_username = ?", (session['username'],))
            classes = cur.fetchall()

            # Sanitize the classes data to ensure it is JSON serializable
            sanitized_classes = []
            for cls in classes:
                sanitized_classes.append([item if item is not None else "" for item in cls])

            return render_template('teacher_dashboard.html', classes=sanitized_classes)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('teacher_dashboard.html', error=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/')




@app.route('/teacher/teacher_profile')
def teacher_profile():
    connection = None
    cur = None

    try:
        connection = db()
        cur = connection.cursor()
        cur.execute("SELECT teacher_name, email, phone FROM teachers WHERE username = ?", (session['username'],))
        profile_data = cur.fetchone()
        return render_template('teacher_profile.html', profile_data=profile_data)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('teacher_profile.html', error=error_message)

    finally:
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()



@app.route('/teacher/update_profile', methods=['POST'])
def update_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    connection = None
    cur = None

    try:
        connection = db()
        cur = connection.cursor()
        cur.execute("UPDATE teachers SET teacher_name = ?, email = ?, phone = ? WHERE username = ?",
                    (name, email, phone, session['username']))
        connection.commit()
        return redirect('/teacher/teacher_profile')

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('teacher_profile.html', error=error_message)

    finally:
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()



@app.route('/teacher/add_class', methods=['GET', 'POST'])
def add_class():
    if 'loggedin' in session and session['role'] == 'teacher':
        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            if request.method == 'POST':
                class_name = request.form['class_name']
                class_section = request.form['class_section']
                attendance_date = request.form['attendance_date']
                cur.execute("INSERT INTO classes (class_sec, class_name, class_date, teacher_username) VALUES (?, ?, ?, ?)",
                            (class_section, class_name, attendance_date, session['username']))
                connection.commit()
                return redirect('/teacher/dashboard')

            cur.execute("SELECT DISTINCT class_sec FROM classes")
            class_sections = cur.fetchall()
            return render_template('add_class.html', class_sections=class_sections)

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return render_template('add_class.html', error=error_message)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/')




@app.route('/teacher/mark_attendance', methods=['GET'])
def mark_attendance():
    if 'loggedin' in session and session['role'] == 'teacher':
        # Retrieve any necessary data for the attendance marking page here if needed
        return render_template('mark_attendance.html')
    else:
        return redirect('/teacher/login')  # Redirect to login if not logged in




@app.route("/teacher/mark_attendance/validate", methods=['POST'])
def validate_class_details():
    if 'loggedin' in session and session['role'] == 'teacher':
        data = request.get_json()
        connection = None
        cur = None

        try:
            class_date = data['date']
            class_name = data['class_name']
            class_sec = data['class_sec']

            connection = db()
            cur = connection.cursor()
            cur.execute("SELECT class_id FROM classes WHERE class_name = ? AND class_sec = ? AND class_date = ?",
                        (class_name, class_sec, class_date))
            class_info = cur.fetchone()

            if class_info:
                class_id = class_info[0]
                cur.execute("SELECT student_id, student_name FROM students WHERE class_sec = ?", (class_sec,))
                students = [{"id": student[0], "name": student[1]} for student in cur.fetchall()]
                return Response(json.dumps({"success": True, "students": students}), status=200, mimetype='application/json')

            return Response(json.dumps({"success": False, "message": "Class not found or invalid date."}), status=404, mimetype='application/json')

        except Exception as e:
            return Response(json.dumps({"success": False, "message": f"An error occurred: {str(e)}"}), status=500, mimetype='application/json')

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()




@app.route("/teacher/mark_attendance/<class_id>", methods=['GET'])
def display_attendance_form(class_id):
    if 'loggedin' in session and session['role'] == 'teacher':
        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            cur.execute("SELECT * FROM classes WHERE class_id = ?", (class_id,))
            classes = cur.fetchone()

            if classes is None:
                return "Class not found", 404

            cur.execute("SELECT * FROM students WHERE class_sec = ?", (classes[3],))
            students = cur.fetchall()

            return render_template('mark_attendance.html', students=students,
                                   class_date=classes[4], class_name=classes[1],
                                   class_sec=classes[3], class_id=classes[0])

        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            return error_message, 500

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/teacher/login')






@app.route("/teacher/mark_attendance/update", methods=['POST'])
def update_attendance():
    if 'loggedin' in session and session['role'] == 'teacher':
        class_date = request.form.get('class_date').strip()
        class_sec = request.form.get('class_sec').strip()
        class_name = request.form.get('class_name').strip()

        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            query = "SELECT class_id FROM classes WHERE class_name = ? AND class_sec = ? AND class_date = ?"
            cur.execute(query, (class_name, class_sec, class_date))
            class_info = cur.fetchone()

            if class_info:
                class_id = class_info[0]

                for student in request.form:
                    if student.startswith('attendance_'):
                        student_id = student.split('_')[1]
                        status = request.form[student]

                        cur.execute("SELECT * FROM attendance WHERE class_id = ? AND student_id = ?",
                                    (class_id, student_id))
                        existing_record = cur.fetchone()

                        if existing_record:
                            cur.execute("UPDATE attendance SET status = ? WHERE class_id = ? AND student_id = ?",
                                        (status, class_id, student_id))
                        else:
                            cur.execute("INSERT INTO attendance (class_id, student_id, status) VALUES (?, ?, ?)",
                                        (class_id, student_id, status))

                connection.commit()
                return make_response(json.dumps({"success": True, "message": "Attendance updated successfully!"}), 200)
            else:
                return make_response(json.dumps({"success": False, "message": "Class not found or invalid date."}), 400)

        except Exception as e:
            return make_response(json.dumps({"success": False, "message": f"An error occurred: {str(e)}"}), 500)

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/teacher/login')



@app.route('/admin/admin_dashboard')
def admin_dashboard():
    if 'loggedin' in session and session['role'] == 'admin':
        return render_template('admin_dashboard.html')
    else:
        return redirect('/')




@app.route("/admin/get_attendance_report", methods=['GET', 'POST'])
def get_attendance_report():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            if request.method == 'POST':
                class_sec = request.form.get('class_sec')
                class_date = request.form.get('class_date')
                class_name = request.form.get('class_name')

                cur.execute("SELECT student_id, student_name FROM students WHERE class_sec = ?", (class_sec,))
                students = cur.fetchall()

                cur.execute("""
                    SELECT student_id, status
                    FROM attendance
                    WHERE class_id IN (
                        SELECT class_id FROM classes
                        WHERE class_sec = ? AND class_date = ? AND class_name = ?
                    )
                """, (class_sec, class_date, class_name))
                attendance = cur.fetchall()

                return render_template('attendance_report.html', class_sec=class_sec, class_date=class_date,
                                       class_name=class_name, students=students, attendance=attendance)

            cur.execute("SELECT DISTINCT class_sec FROM classes")
            class_secs = cur.fetchall()

            cur.execute("SELECT DISTINCT class_name FROM classes")
            class_names = cur.fetchall()

            return render_template('attendance_report.html', class_secs=class_secs, class_names=class_names)

        except Exception as e:
            return render_template('attendance_report.html', error=f"An error occurred: {str(e)}")

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/admin/login')





@app.route('/admin/admin_profile')
def admin_profile():
    connection = None
    cur = None

    try:
        connection = db()
        cur = connection.cursor()
        cur.execute("SELECT admin_name, email, phone FROM admins WHERE username = ?", (session['username'],))
        profile_data = cur.fetchone()
        return render_template('admin_profile.html', profile_data=profile_data)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('admin_profile.html', error=error_message)

    finally:
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()


@app.route('/admin/update_admin_profile', methods=['POST'])
def update_admin_profile():
    name = request.form.get('name')
    email = request.form.get('email')
    phone = request.form.get('phone')

    connection = None
    cur = None

    try:
        connection = db()
        cur = connection.cursor()
        cur.execute("UPDATE admins SET admin_name = ?, email = ?, phone = ? WHERE username = ?",
                    (name, email, phone, session['username']))
        connection.commit()
        return redirect('/admin/admin_profile')

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return render_template('admin_profile.html', error=error_message)

    finally:
        if cur is not None:
            cur.close()
        if connection is not None:
            connection.close()



@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    session.pop('role', None)
    return redirect('/')


@app.route('/admin/student_report', methods=['GET', 'POST'])
def student_report():
    if 'loggedin' in session and session['role'] == 'admin':
        connection = None
        cur = None

        try:
            connection = db()
            cur = connection.cursor()

            if request.method == 'POST':
                student_id = request.form['student_id']
                cur.execute("SELECT student_id, student_name FROM students WHERE student_id = ?", (student_id,))
                stud = cur.fetchone()

                cur.execute("""
                    SELECT classes.class_date, classes.class_id, classes.class_name, attendance.status
                    FROM attendance
                    JOIN classes ON attendance.class_id = classes.class_id
                    WHERE attendance.student_id = ?
                """, (student_id,))
                attn = cur.fetchall()

                if stud and attn:
                    total_classes = len(attn)
                    attended_classes = sum(1 for entry in attn if entry[3] == 'present')
                    p = (attended_classes / total_classes) * 100 if total_classes > 0 else 0
                    return render_template('student_attendance.html', stud=stud, attn=attn, p=p)

                error = "No records found for the given student ID."
                return render_template('student_attendance.html', error=error)

            return render_template('student_attendance.html')

        except Exception as e:
            return render_template('student_attendance.html', error=f"An error occurred: {str(e)}")

        finally:
            if cur is not None:
                cur.close()
            if connection is not None:
                connection.close()

    return redirect('/admin/login')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8000')
