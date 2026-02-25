import json
from datetime import datetime, timedelta

#класс для описания задачи
class Task:
    def __init__(self, name: str, description: str, priority: int, days, hours, minutes):
        self.name = name
        self.description = description
        self.priority = priority
        if days == 0 and hours == 0 and minutes == 0:
            self.deadline = 'Нет'
        else:
            self.deadline = str(datetime.now() + timedelta(days=days, hours=hours, minutes=minutes))
        self.status = 'not started'
        self.flag = False

    #добавление задачи
    def add_task(self):
        try:
            with open('tasks.json', 'r') as f:
                tasks = json.load(f)
            f.close()
        except Exception:
                tasks = list()
        task = {
            'id': len(tasks) + 1, 
            'name': self.name, 
            'description': self.description,
            'priority': self.priority,
            'deadline': self.deadline,
            'status': self.status,
            'flag': self.flag
        }
        tasks.append(task)
        with open('tasks.json', 'w') as f:
            json.dump(tasks, f, indent=4)
        f.close()

    


#удаление задачи
def delete_task(id: int):
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            del tasks[i]
            break
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    f.close()

#отметка задачи как "в процессе"
def update_in_process(id: int):
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            tasks[i]['status'] = 'in process'
            break
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    f.close()

#отметка задачи как "сделано"
def update_done(id: int):
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            tasks[i]['status'] = 'done'
            break
    with open('tasks.json', 'w') as f:
        json.dump(tasks, f, indent=4)
    f.close()

#получение еще не начатых задач
def get_not_started():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'not started':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])

#получение задач со статусом "в процессе"
def get_in_process():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'in process':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])

#получение сделанных задач
def get_done():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'done':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])