import tkinter as tk
from studentmanagement import DatabaseApp


def open_main_app(conn):
    root = tk.Tk()
    app = DatabaseApp(root, conn)  # Truyền kết nối đến DatabaseApp
    root.mainloop()
