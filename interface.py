import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import model


#класс приложения tkinter
class TaskApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Таск-трекер")

        #фрейм создания задачи
        top_frame = tk.Frame(master)
        top_frame.pack(pady=15)

        #кнопка создания задачи
        self.add_button = tk.Button(
            top_frame, text="Создать задачу", command=self.show_create_task_dialog
        )
        self.add_button.pack(fill="x")

        #основной фрейм
        canvas = tk.Canvas(master)
        scrollbar = tk.Scrollbar(master, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda x: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="center")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 30), pady=20)

        #секции задач разных типов
        self.section_not_started = tk.LabelFrame(
            scrollable_frame, text="Не начато:", font=("Times New Roman", 14, "bold"), bg='red', fg='black'
        )
        self.section_not_started.pack(fill="x", pady=(0, 10))

        self.section_in_process = tk.LabelFrame(
            scrollable_frame, text="В процессе:", font=("Times New Roman", 14, "bold"), bg='yellow', fg='black'
        )
        self.section_in_process.pack(fill="x", pady=(0, 10))

        self.section_done = tk.LabelFrame(
            scrollable_frame, text="Сделаны:", font=("Times New Roman", 14, "bold"), bg='green', fg='black'
        )
        self.section_done.pack(fill="x", pady=(0, 10))

        #инициализация списков задач с использованием функций из model.py
        self._refresh_sections_from_model()

    #функция по отображению задачи
    def _create_task_row(self, parent, task):
        row = tk.Frame(parent)
        row.pack(fill="x", pady=3, padx=5)

        task_id = task["id"]
        status = task.get("status", "not started")

        #считывание и преобразование дедлайна из str в datetime, подсчет не истек ли дедлайн
        deadline = task.get('deadline')
        is_exceeded = False
        if deadline != 'Нет':
            deadline_dt = datetime.strptime(deadline.split(".")[0], "%Y-%m-%d %H:%M:%S")
            if (deadline_dt - datetime.now()).total_seconds() <= 3600:
                is_exceeded = True
            deadline_dt = deadline_dt.strftime("%d.%m.%Y %H:%M")
        else:
            deadline_dt = deadline
        if status == 'done':
            color = 'black'
        elif is_exceeded:
            color = 'red'
        else:
            color = 'black'

        #строка с информацией о задаче
        if task['priority'] == 1:
            priority_showed = 'ОЧЕНЬ СРОЧНО'
        elif task['priority'] == 2:
            priority_showed = 'Средняя срочность'
        else:
            priority_showed = 'Не срочно'
        info_text = f"•{task['name']} | Уровень срочности: {priority_showed}"
        lbl = tk.Label(row, text=info_text, anchor="w", fg=color)
        lbl.pack(side="left", fill="x", expand=True)

        #кнопка "в процессе"
        in_proc_btn = tk.Button(
            row,
            text="В процессе⌛",
            width=11,
            command=lambda tid=task_id: self._on_mark_in_process(tid),
        )

        #кнопка "Сделано"
        done_btn = tk.Button(
            row,
            text="Сделано✅",
            width=11,
            command=lambda tid=task_id: self._on_mark_done(tid),
        )
        

        #кнопка удаления
        del_btn = tk.Button(
            row,
            text="Удалить🗑️",
            width=11,
            command=lambda tid=task_id: self._on_delete(tid),
        )

        #кнопка описания
        desc_text = task.get("description", "Нет описания")
        desc_btn = tk.Button(
            row,
            text="Описание🗒️",
            width=11,
            command=lambda name=task["name"], d=desc_text: self._show_description(name, d),
        )
        #отображение дедлайна
        deadline_lbl = tk.Label(row, text=f'Дедлайн: {deadline_dt}', fg=color, font=("Arial", 9))
        deadline_lbl.pack(side="right", padx=(0, 15))

        #упаковка кнопок, отключение ненужных
        desc_btn.pack(side="right", padx=2)
        del_btn.pack(side="right", padx=2)
        done_btn.pack(side="right", padx=2)
        if status == "done":
            done_btn.config(state="disabled")
            deadline_lbl.pack_forget()
        in_proc_btn.pack(side="right", padx=2)
        if status == 'in process' or status == 'done':
            in_proc_btn.config(state="disabled")


    #функция для описания
    def _show_description(self, task_name, description):
        messagebox.showinfo(f"Задача: {task_name}", description)

    #очищение секции задач
    def _clear_section(self, section):
        for widget in section.winfo_children():
            widget.destroy()

    #функция обновления секций
    def _refresh_sections_from_model(self):
        self._clear_section(self.section_not_started)
        self._clear_section(self.section_in_process)
        self._clear_section(self.section_done)

        not_started = model.get_not_started()
        in_process = model.get_in_process()
        done = model.get_done()

        if len(not_started) == 0:
            self.section_not_started.pack_forget()
        else:
            self.section_not_started.pack(fill="x", pady=(0, 10))
            for task in not_started:
                self._create_task_row(self.section_not_started, task)
        if len(in_process) == 0:
            self.section_in_process.pack_forget()
        else:
            self.section_in_process.pack(fill='x', pady=(0, 10))
            for task in in_process:
                self._create_task_row(self.section_in_process, task)
        if len(done) == 0:
            self.section_done.pack_forget()
        else:
            self.section_done.pack(fill='x', pady=(0, 10))
            for task in done:
                self._create_task_row(self.section_done, task)

    #функции по обновлению задач каждого отдельного статуса
    def _on_mark_in_process(self, task_id: int):
        model.update_in_process(task_id)
        self._refresh_sections_from_model()

    def _on_mark_done(self, task_id: int):
        model.update_done(task_id)
        self._refresh_sections_from_model()

    def _on_delete(self, task_id: int):
        model.delete_task(task_id)
        self._refresh_sections_from_model()

    #диалог по созданию новой задачи
    def show_create_task_dialog(self):
        dialog = tk.Toplevel(self.master)
        dialog.title("Создать задачу")
        dialog.geometry("350x220")
        dialog.transient(self.master)
        dialog.grab_set()

        tk.Label(dialog, text="Название:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = tk.Entry(dialog, width=35)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Описание:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )
        desc_entry = tk.Entry(dialog, width=35)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Срочность (1-3):").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )
        priority_entry = tk.Entry(dialog, width=10)
        priority_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        tk.Label(dialog, text="Время до дедлайна дней/часов/минут:").grid(
            row=3, column=0, sticky="w", padx=10, pady=5
        )
        time_frame = tk.Frame(dialog)
        time_frame.grid(row=3, column=1, columnspan=2, sticky="w", pady=5)
        days_entry = tk.Entry(time_frame, width=3)
        days_entry.grid(row=0, column=0, padx=1)
        hours_entry = tk.Entry(time_frame, width=3)
        hours_entry.grid(row=0, column=1, padx=4)
        minutes_entry = tk.Entry(time_frame, width=3)
        minutes_entry.grid(row=0, column=2, padx=4)

        #функция по созданию задачи с введенными данными
        def on_create():
            name = name_entry.get().strip()
            if len(desc_entry.get()) > 0:
                description = desc_entry.get().rstrip()
            else:
                description = 'Нет описания задачи.'
            if not name:
                messagebox.showwarning("Ошибка!", "Введите имя задачи.")
                return
            try:
                priority = int(priority_entry.get())
            except ValueError:
                messagebox.showerror("Ошибка!", "Значение срочности отсутствует или имеет неверный тип.")
                return
            except priority not in [1, 2, 3]:
                messagebox.showerror("Ошибка!", "Значение срочности должн0 быть в диапазоне от 1 до 3.")
                return

            if len(days_entry.get()) > 0:
                days = int(days_entry.get())
            else:
                days = 0
            if len(hours_entry.get()) > 0:
                hours = int(hours_entry.get())
            else:
                hours = 0
            if len(minutes_entry.get()) > 0:
                minutes = int(minutes_entry.get())
            else:
                minutes = 0

            #создание объекта Task на основе введенных данных
            task = model.Task(
                name=name,
                description=description,
                priority=priority,
                days=days,
                hours=hours,
                minutes=minutes,
            )
            task.add_task()
            self._refresh_sections_from_model()
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        #вспомогательные кнопки диалога
        tk.Button(btn_frame, text="Создать", command=on_create).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT)
