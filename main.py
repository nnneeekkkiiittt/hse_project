from model import Task
from interface import TaskApp
import tkinter as tk


#запуск программы: создание приложения класса, описанного в interface.py
if __name__ == '__main__':
    root = tk.Tk()
    app = TaskApp(root)
    root.resizable(True, True)
    screen_width = int(root.winfo_screenwidth() * 0.8)
    screen_height = int(root.winfo_screenheight() * 0.8)
    root.geometry(f'{screen_width}x{screen_height}')
    root.mainloop()
