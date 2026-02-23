import tkinter as tk
from tkinter import messagebox
import json
from model import *


class TaskApp:
    def __init__(self, master, filename='tasks.json'):
        self.master = master
        self.master.title("Task Manager")
        self.filename = filename

        # Top frame with Create Task button
        top_frame = tk.Frame(master)
        top_frame.pack(pady=15)

        self.add_button = tk.Button(
            top_frame, text="Create Task", command=self.show_create_task_dialog
        )
        self.add_button.pack()

        # Scrollable center frame
        canvas = tk.Canvas(master)
        scrollbar = tk.Scrollbar(master, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(30, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 30), pady=20)

        # Task sections
        self.section_not_started = tk.LabelFrame(
            scrollable_frame, text="Not Started", font=("Arial", 11, "bold")
        )
        self.section_not_started.pack(fill="x", pady=(0, 10))

        self.section_in_process = tk.LabelFrame(
            scrollable_frame, text="In Process", font=("Arial", 11, "bold")
        )
        self.section_in_process.pack(fill="x", pady=(0, 10))

        self.section_done = tk.LabelFrame(
            scrollable_frame, text="Done", font=("Arial", 11, "bold")
        )
        self.section_done.pack(fill="x", pady=(0, 10))

        self.update_task_list()

    def _create_task_row(self, parent, task):
        """Creates a row with task info and action buttons."""
        row = tk.Frame(parent)
        row.pack(fill="x", pady=3, padx=5)

        task_id = task["id"]
        status = task.get("status", "not started")

        # Task info (click to view description)
        info_text = f"#{task_id} {task['name']} | Priority: {task['priority']}"
        lbl = tk.Label(row, text=info_text, anchor="w", cursor="hand2")
        lbl.pack(side="left", fill="x", expand=True)
        desc = task.get("description", "(no description)")
        lbl.bind(
            "<Button-1>",
            lambda e, name=task["name"], d=desc: self._show_description(name, d),
        )

        # In Process button (disabled when already in process or done)
        in_proc_btn = tk.Button(
            row,
            text="In Process",
            width=10,
            command=lambda: self._mark_in_process(task_id),
        )
        in_proc_btn.pack(side="right", padx=2)
        if status in ("in process", "done"):
            in_proc_btn.config(state="disabled")

        # Done button (disabled when already done)
        done_btn = tk.Button(
            row,
            text="Done",
            width=8,
            command=lambda: self._mark_done(task_id),
        )
        done_btn.pack(side="right", padx=2)
        if status == "done":
            done_btn.config(state="disabled")

        # Delete button
        del_btn = tk.Button(
            row,
            text="🗑️",
            width=6,
            command=lambda: self._delete_task(task_id),
        )
        del_btn.pack(side="right", padx=2)

    def _show_description(self, task_name, description):
        """Shows task description in a message dialog."""
        messagebox.showinfo(f"Task: {task_name}", description)

    def _mark_in_process(self, task_id):
        update_in_process(task_id)
        self.update_task_list()

    def _mark_done(self, task_id):
        update_done(task_id)
        self.update_task_list()

    def _clear_section(self, section):
        for widget in section.winfo_children():
            widget.destroy()

    def show_create_task_dialog(self):
        """Opens a dialog to create a new task."""
        dialog = tk.Toplevel(self.master)
        dialog.title("Create Task")
        dialog.geometry("350x220")
        dialog.transient(self.master)
        dialog.grab_set()

        tk.Label(dialog, text="Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        name_entry = tk.Entry(dialog, width=35)
        name_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Description:").grid(
            row=1, column=0, sticky="w", padx=10, pady=5
        )
        desc_entry = tk.Entry(dialog, width=35)
        desc_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(dialog, text="Priority (1-10):").grid(
            row=2, column=0, sticky="w", padx=10, pady=5
        )
        priority_entry = tk.Entry(dialog, width=10)
        priority_entry.insert(0, "5")
        priority_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        tk.Label(dialog, text="Days until deadline:").grid(
            row=3, column=0, sticky="w", padx=10, pady=5
        )
        days_entry = tk.Entry(dialog, width=10)
        days_entry.insert(0, "0")
        days_entry.grid(row=3, column=1, sticky="w", padx=10, pady=5)

        def on_create():
            name = name_entry.get().strip()
            description = desc_entry.get().strip()
            if not name:
                messagebox.showwarning("Warning", "Please enter a task name.")
                return
            try:
                priority = int(priority_entry.get())
                days = int(days_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Priority and days must be numbers.")
                return
            task = Task(name=name, description=description, priority=priority, days=days)
            task.add_task()
            self.update_task_list()
            dialog.destroy()

        btn_frame = tk.Frame(dialog)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Create", command=on_create).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT)

    def _delete_task(self, task_id):
        """Deletes a task by id using model.delete_task."""
        delete_task(task_id)
        self.update_task_list()

    def update_task_list(self):
        """Refreshes the task list from tasks.json, grouped by status."""
        self._clear_section(self.section_not_started)
        self._clear_section(self.section_in_process)
        self._clear_section(self.section_done)

        try:
            with open(self.filename, "r") as f:
                tasks = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            tasks = []

        for task in tasks:
            status = task.get("status", "not started")
            # Normalize status for grouping (model uses "in process" with space)
            if status in ("in process", "inprogress"):
                status = "in process"
            elif status in ("not started", "notstarted"):
                status = "not started"

            if status == "not started":
                self._create_task_row(self.section_not_started, task)
            elif status == "in process":
                self._create_task_row(self.section_in_process, task)
            else:  # done
                self._create_task_row(self.section_done, task)
