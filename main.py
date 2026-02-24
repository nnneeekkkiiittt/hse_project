from model import Task
from interface import TaskApp
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    app = TaskApp(root, 'tasks.json')
    root.resizable(False, True)
    root.mainloop()
