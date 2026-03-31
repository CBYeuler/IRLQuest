import json
import math
class User:
    def __init__(self):
        self.level = 1
        self.totalXP = 0
        self.stats = {
            "Strength":0,
            "Discipline":0,
            "Mind":0,
            "Faith":0,
            "Social":0,
            "Skill":0
        }
        self.tasks = []

    def load(self):
        with open('data.json', 'r') as f:
            data = json.load(f)
            self.level = data["level"]
            self.totalXP = data["totalXP"]
            self.stats = data["stats"]
            self.tasks = data["tasks"] 
    
    def save(self):
        data = {
            "level": self.level,
            "totalXP":self.totalXP,
            "stats":self.stats,
            "tasks":self.tasks
        }
        with open('data.json','w',encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_task(self, name, xp, stat):
        new_id = max((t["id"] for t in self.tasks), default=0) + 1
        self.tasks.append({
            "id":new_id,
            "name":name,
            "xp":xp,
            "stat":stat,
            "completed":False
        })
        self.save()
        print(f"Task '{name}' added!")


    def complete_task(self, id):
        
        task = next((t for t in self.tasks if t['id'] == id),None)
        if task is None:
            print(f" No task found with ID {id}")
            return
        else:
            task['completed'] == True
            task_xp = task["xp"]
            task_stat = task["stat"]

            self.totalXP += task_xp
            self.stats[task_stat] += task_xp
            self.level = math.floor(self.totalXP/100)

            self.save()
            print(f"Task '{task['name']}' completed! +{task_xp} XP → {task_stat}")

            


