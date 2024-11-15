import tkinter as tk
from tkinter import messagebox, ttk
from psycopg2 import sql


class DatabaseApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.cur = self.conn.cursor()
        self.create_table()  # Create the table if it doesn't exist
        self.root.title("Student Management")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        self.create_widgets()
        self.reload_list()
        self.entry_name = None
        self.entry_age = None
        self.entry_gender = None
        self.entry_major = None

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            age INTEGER NOT NULL,
            gender VARCHAR(10) NOT NULL,
            major VARCHAR(100) NOT NULL
        );
        """
        self.cur.execute(create_table_query)
        self.conn.commit()

    def create_widgets(self):
        # Tạo style cho các nút
        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 10, "bold"),
                        background="#FFC0CB", foreground="black", padding=6)
        style.map("TButton", background=[
                  ('active', '#45a049')], relief=[('pressed', 'sunken')])

        tab_control = ttk.Notebook(self.root)
        tab_control.pack(expand=1, fill="both")

        # Tab quản lý sinh viên
        tab_students = ttk.Frame(tab_control)
        tab_control.add(tab_students, text="Students")

        # Tab hiển thị sinh viên theo chuyên ngành
        tab_show_students = ttk.Frame(tab_control)
        tab_control.add(tab_show_students, text="Show Students by Major")

        # Frame đầu tiên để nhập thông tin (2 dòng)
        frame_top = tk.Frame(tab_students, bg='#f0f0f0')
        frame_top.pack(pady=10)

        label_name = tk.Label(frame_top, text="Name:", bg='#f0f0f0')
        label_name.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.entry_name = tk.Entry(frame_top)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        label_age = tk.Label(frame_top, text="Age:", bg='#f0f0f0')
        label_age.grid(row=0, column=2, padx=5, pady=5, sticky="w")
        self.entry_age = tk.Entry(frame_top)
        self.entry_age.grid(row=0, column=3, padx=5, pady=5)

        label_gender = tk.Label(frame_top, text="Gender:", bg='#f0f0f0')
        label_gender.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.entry_gender = tk.Entry(frame_top)
        self.entry_gender.grid(row=1, column=1, padx=5, pady=5)

        label_major = tk.Label(frame_top, text="Major:", bg='#f0f0f0')
        label_major.grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.entry_major = tk.Entry(frame_top)
        self.entry_major.grid(row=1, column=3, padx=5, pady=5)
        # Frame giữa để chứa các nút chức năng
        frame_buttons = tk.Frame(tab_students, bg='#f0f0f0')
        frame_buttons.pack(pady=10)

        button_width = 15
        btn_add = ttk.Button(
            frame_buttons, text="Add Student", command=self.add_student)
        btn_add.grid(row=0, column=0, padx=5, pady=5)

        btn_update = ttk.Button(
            frame_buttons, text="Update Student", command=self.update_student)
        btn_update.grid(row=0, column=1, padx=5, pady=5)

        btn_delete = ttk.Button(
            frame_buttons, text="Delete Student", command=self.delete_student)
        btn_delete.grid(row=0, column=2, padx=5, pady=5)

        btn_reload = ttk.Button(
            frame_buttons, text="Reload List", command=self.reload_list)
        btn_reload.grid(row=0, column=3, padx=5, pady=5)

        # Frame dưới để chứa danh sách sinh viên
        frame_bottom = tk.Frame(tab_students)
        frame_bottom.pack(pady=10, padx=10, fill='both', expand=True)

        self.tree = ttk.Treeview(frame_bottom, columns=(
            "ID", "Name", "Age", "Gender", "Major"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Major", text="Major")

        self.tree.column("ID", anchor="center", width=50)
        self.tree.column("Name", anchor="center", width=150)
        self.tree.column("Age", anchor="center", width=50)
        self.tree.column("Gender", anchor="center", width=100)
        self.tree.column("Major", anchor="center", width=150)

        self.tree.pack(padx=10, pady=5, fill='both', expand=True)

        # Add a scrollbar for the Treeview
        self.scrollbar = ttk.Scrollbar(
            frame_bottom, orient="vertical", command=self.tree.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Tab thứ hai để chọn ngành
        label_select_major = tk.Label(
            tab_show_students, text="Select Major:", bg='#f0f0f0')
        label_select_major.pack(pady=5)

        self.combo_select_major = ttk.Combobox(tab_show_students, values=[
            "Công nghệ thông tin", "Quan hệ công chúng", "Thiết kế", "Quản trị kinh doanh", "Kế toán", "Cơ khí - Điện tử"])
        self.combo_select_major.pack(pady=5)

        btn_show_students = ttk.Button(
            tab_show_students, text="Show Students", command=self.show_students_by_major)
        btn_show_students.pack(pady=5)

        # Treeview để hiển thị thông tin sinh viên theo ngành
        self.tree_major = ttk.Treeview(tab_show_students, columns=(
            "ID", "Name", "Age", "Gender", "Teacher", "Course Code"), show="headings")
        self.tree_major.heading("ID", text="ID")
        self.tree_major.heading("Name", text="Name")
        self.tree_major.heading("Age", text="Age")
        self.tree_major.heading("Gender", text="Gender")
        self.tree_major.heading("Teacher", text="Teacher")
        self.tree_major.heading("Course Code", text="Course Code")

        self.tree_major.column("ID", anchor="center", width=50)
        self.tree_major.column("Name", anchor="center", width=150)
        self.tree_major.column("Age", anchor="center", width=50)
        self.tree_major.column("Gender", anchor="center", width=100)
        self.tree_major.column("Teacher", anchor="center", width=150)
        self.tree_major.column("Course Code", anchor="center", width=150)

        self.tree_major.pack(padx=10, pady=5)

    def add_student(self):
        name = self.entry_name.get()
        try:
            age = int(self.entry_age.get())
        except ValueError:
            messagebox.showwarning("Input Error", "Age must be a number.")
            return
        gender = self.entry_gender.get()
        major = self.entry_major.get()
        if name and age and gender and major:
            self.cur.execute(
                "INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)", (name, age, gender, major))
            self.conn.commit()
            messagebox.showinfo("Success", "Student added successfully!")
            self.reload_list()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def update_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])['values'][0]
            name = self.entry_name.get()
            try:
                age = int(self.entry_age.get())
            except ValueError:
                messagebox.showwarning("Input Error", "Age must be a number.")
                return
            gender = self.entry_gender.get()
            major = self.entry_major.get()
            if name and age and gender and major:
                self.cur.execute("UPDATE students SET name=%s, age=%s, gender=%s, major=%s WHERE id=%s", (
                    name, age, gender, major, student_id))
                self.conn.commit()
                messagebox.showinfo("Success", "Student updated successfully!")
                self.reload_list()
            else:
                messagebox.showwarning(
                    "Input Error", "Please fill in all fields.")
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a student to update.")

    def delete_student(self):
        selected = self.tree.selection()
        if selected:
            student_id = self.tree.item(selected[0])['values'][0]
            self.cur.execute("DELETE FROM students WHERE id=%s", (student_id,))
            self.conn.commit()
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.reload_list()
        else:
            messagebox.showwarning(
                "Selection Error", "Please select a student to delete.")

    def reload_list(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.cur.execute("SELECT * FROM students")
        for row in self.cur.fetchall():
            self.tree.insert("", tk.END, values=row)

    def show_students_by_major(self):
        major = self.combo_select_major.get()
        for row in self.tree_major.get_children():
            self.tree_major.delete(row)

        self.cur.execute("""
            SELECT s.id, s.name, s.age, s.gender, c.teacher, c.course_code
            FROM students s
            JOIN classes c ON s.major = c.major
            WHERE s.major = %s
        """, (major,))

        for row in self.cur.fetchall():
            self.tree_major.insert("", tk.END, values=row)

    def on_closing(self):
        self.cur.close()
        self.conn.close()
        self.root.destroy()
