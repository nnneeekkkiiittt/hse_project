import json


class Task:
    def __init__(self, name: str, description: str, priority: int, deadline: str):
        self.name = name
        self.description = description
        self.priority = priority
        self.deadline = deadline
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


    

new_task = Task(name='task1', description='some description', priority='urgent!!!', deadline='now!!!')
new_task.add_task()
print('successfully added')