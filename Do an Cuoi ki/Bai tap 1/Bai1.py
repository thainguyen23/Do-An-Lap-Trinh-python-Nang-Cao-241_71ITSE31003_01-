import tkinter as tk
from tkinter import ttk, Menu
from tkinter import messagebox as msg


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GUI Calculator")
        self.history = []  # Danh sách lưu trữ lịch sử

        # Tạo menu
        self.create_menu()

        # Tạo tab
        self.create_tabs()

        # Tạo các thành phần giao diện
        self.create_widgets()

    def create_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def create_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, expand=True)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        self.notebook.add(self.tab1, text="Calculator")
        self.notebook.add(self.tab2, text="History")

    def create_widgets(self):
        self.frame = ttk.Frame(self.tab1)
        self.frame.pack(padx=10, pady=10)

        self.num1_label = ttk.Label(self.frame, text="Number 1:")
        self.num1_label.grid(row=0, column=0, padx=5, pady=5)

        self.num1_entry = ttk.Entry(self.frame)
        self.num1_entry.grid(row=0, column=1, padx=5, pady=5)

        self.num2_label = ttk.Label(self.frame, text="Number 2:")
        self.num2_label.grid(row=1, column=0, padx=5, pady=5)

        self.num2_entry = ttk.Entry(self.frame)
        self.num2_entry.grid(row=1, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.frame, text="Add", command=self.add)
        self.add_button.grid(row=2, column=0, padx=5, pady=5)

        self.subtract_button = ttk.Button(
            self.frame, text="Subtract", command=self.subtract)
        self.subtract_button.grid(row=2, column=1, padx=5, pady=5)

        self.multiply_button = ttk.Button(
            self.frame, text="Multiply", command=self.multiply)
        self.multiply_button.grid(row=3, column=0, padx=5, pady=5)

        self.divide_button = ttk.Button(
            self.frame, text="Divide", command=self.divide)
        self.divide_button.grid(row=3, column=1, padx=5, pady=5)

        self.result_label = ttk.Label(self.frame, text="Result: ")
        self.result_label.grid(row=4, column=0, columnspan=2, pady=10)

        # Tạo Listbox để hiển thị lịch sử trong tab2
        self.history_listbox = tk.Listbox(self.tab2)
        self.history_listbox.pack(padx=10, pady=10, fill="both", expand=True)

    def show_about(self):
        tk.messagebox.showinfo("About", "neyugn <3 \n2274802010587")

    def add(self):
        self.calculate_result('+')

    def subtract(self):
        self.calculate_result('-')

    def multiply(self):
        self.calculate_result('*')

    def divide(self):
        self.calculate_result('/')

    def calculate_result(self, operator):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            if operator == '+':
                result = num1 + num2
            elif operator == '-':
                result = num1 - num2
            elif operator == '*':
                result = num1 * num2
            elif operator == '/':
                if num2 == 0:
                    self.result_label.config(text="Error: Division by zero")
                    return
                result = num1 / num2
            self.result_label.config(text=f"Result: {result}")

            # Thêm phép tính vào lịch sử và cập nhật Listbox
            history_entry = f"{num1} {operator} {num2} = {result}"
            self.history.append(history_entry)
            self.history_listbox.insert(tk.END, history_entry)
        except ValueError:
            self.result_label.config(text="Error: Invalid")


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
