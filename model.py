import json
from datetime import datetime, timedelta


class Task:
    def __init__(self, name: str, description: str, priority: int, days=0, hours=0, minutes=0):
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = str(datetime.now() + timedelta(days=days, hours=hours, minutes=minutes))
        self.status = 'not started'
        self.flag = False


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

def get_not_started():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'not started':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])

def get_in_process():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'in process':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])

def get_done():
    res = list()
    with open('tasks.json', 'r') as f:
        tasks = json.load(f)
    f.close()
    for task in tasks:
        if task['status'] == 'done':
            res.append(task)
    return sorted(res, key=lambda x: x['priority'])