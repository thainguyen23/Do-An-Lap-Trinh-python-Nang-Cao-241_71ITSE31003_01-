from flask import Flask, render_template, redirect, url_for, request, flash, session
from db import connect_to_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            conn = connect_to_db()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
                user = cur.fetchone()

                if user:
                    session['username'] = username
                    return redirect(url_for('student_management'))
                else:
                    flash("Thông tin đăng nhập không hợp lệ!", "danger")

        except Exception as e:
            flash(f"Không thể kết nối cơ sở dữ liệu: {e}", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash("Mật khẩu không khớp!", "danger")
            return render_template('register.html')

        try:
            conn = connect_to_db()
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM users WHERE username=%s", (username,))
                existing_user = cur.fetchone()

                if existing_user:
                    flash("Tài khoản đã tồn tại!", "danger")
                else:
                    cur.execute(
                        "INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                    conn.commit()
                    flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.", "success")
                    return redirect(url_for('login'))

        except Exception as e:
            flash(f"Không thể kết nối cơ sở dữ liệu: {e}", "danger")

    return render_template('register.html')


@app.route('/student_management', methods=['GET', 'POST'])
def student_management():
    if 'username' not in session:
        return redirect(url_for('login'))

    try:
        with connect_to_db() as conn:
            with conn.cursor() as cur:
                if request.method == 'POST':
                    action = request.form.get('action')
                    name = request.form.get('name')
                    age = request.form.get('age')
                    gender = request.form.get('gender')
                    major = request.form.get('major')
                    # Lấy mã số sinh viên (MSSV)
                    mssv = request.form.get('mssv')
                    student_id = request.form.get('student_id')

                    # Kiểm tra nếu MSSV trống
                    if not mssv:
                        flash("Mã số sinh viên không được để trống.", "danger")
                        return redirect(url_for('student_management'))

                    # Kiểm tra tuổi hợp lệ
                    if age:
                        try:
                            age = int(age)
                            if age < 18 or age > 100:
                                flash(
                                    "Tuổi sinh viên phải lớn hơn 18 và nhỏ hơn hoặc bằng 100.", "danger")
                                return redirect(url_for('student_management'))
                        except ValueError:
                            flash("Tuổi không hợp lệ.", "danger")
                            return redirect(url_for('student_management'))

                    # Kiểm tra mã số sinh viên có trùng không
                    if action == 'add':
                        # Kiểm tra MSSV đã tồn tại chưa
                        cur.execute(
                            "SELECT * FROM students WHERE mssv=%s", (mssv,))
                        existing_mssv = cur.fetchone()
                        if existing_mssv:
                            flash(
                                "Mã số sinh viên đã tồn tại! Vui lòng nhập lại.", "danger")
                            return redirect(url_for('student_management'))

                        # Lấy ID sinh viên lớn nhất hiện tại trong bảng
                        cur.execute("SELECT MAX(id) FROM students")
                        max_id = cur.fetchone()[0]
                        # Nếu bảng rỗng thì ID bắt đầu từ 1
                        new_id = max_id + 1 if max_id is not None else 1

                        # Thêm sinh viên mới với ID và MSSV tự động
                        cur.execute(
                            "INSERT INTO students (id, name, age, gender, major, mssv) VALUES (%s, %s, %s, %s, %s, %s)",
                            (new_id, name, age, gender, major, mssv)
                        )
                        flash("Sinh viên đã được thêm thành công!", "success")

                    # Cập nhật sinh viên
                    elif action == 'update' and student_id:
                        try:
                            student_id = int(student_id)
                            cur.execute("UPDATE students SET name=%s, age=%s, gender=%s, major=%s, mssv=%s WHERE id=%s",
                                        (name, age, gender, major, mssv, student_id))
                            flash(
                                "Sinh viên đã được cập nhật thành công!", "success")
                        except ValueError:
                            flash("ID sinh viên không hợp lệ.", "danger")

                    # Xóa sinh viên
                    elif action == 'delete' and student_id:
                        try:
                            student_id = int(student_id)
                            cur.execute(
                                "DELETE FROM students WHERE id=%s", (student_id,))
                            flash("Sinh viên đã được xóa thành công!", "success")
                        except ValueError:
                            flash("ID sinh viên không hợp lệ.", "danger")

                    # Cập nhật lại các ID sinh viên theo thứ tự
                    elif action == 'reload':
                        cur.execute("SELECT id FROM students ORDER BY id")
                        students = cur.fetchall()
                        for index, (student_id,) in enumerate(students, start=1):
                            cur.execute(
                                "UPDATE students SET id=%s WHERE id=%s", (index, student_id))
                        flash("Cập nhật lại ID sinh viên thành công!", "success")

                # Lấy danh sách sinh viên và render lại
                cur.execute("SELECT * FROM students ORDER BY id")
                students = cur.fetchall()

    except Exception as e:
        flash(f"Error connecting to database: {e}", "danger")

    return render_template('student_management.html', students=students)


@app.route('/logout')
def logout():
    # Xóa thông tin người dùng khỏi session
    session.pop('username', None)
    flash("Bạn đã đăng xuất thành công!", "success")
    return redirect(url_for('login'))
