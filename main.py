from model import Task
from interface import TaskApp
import tkinter as tk

#запуск программы: создание приложения
if __name__ == '__main__':
    root = tk.Tk()
    app = TaskApp(root, 'tasks.json')
    root.resizable(True, True)
    root.mainloop()
