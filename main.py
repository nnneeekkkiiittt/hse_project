from model import Task
from interface import TaskApp
import tkinter as tk

#запуск программы: создание приложения класса, описанного в interface.py
if __name__ == '__main__':
    root = tk.Tk()
    app = TaskApp(root, 'tasks.json')
    root.resizable(True, True)
    root.mainloop()
