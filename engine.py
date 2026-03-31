import json
import math
import matplotlib.pyplot as plt
import numpy as np
import subprocess
class User:
    def __init__(self):
        self.name = ""
        self.player_class = ""
        self.motto = ""
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
            self.name = data["name"]
            self.player_class = data["player_class"]
            self.motto = data["motto"]
    
    def save(self):
        data = {
            "level": self.level,
            "totalXP":self.totalXP,
            "stats":self.stats,
            "tasks":self.tasks,
            "name": self.name,
            "player_class": self.player_class,
            "motto": self.motto,
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
    def show_radar(self):
        labels = list(self.stats.keys())
        values = list(self.stats.values())

        N = len(labels)

        values += values[:1]

        angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        ax.fill(angles, values, alpha=0.25, color='blue')
        ax.plot(angles, values, color='blue', linewidth=2)

        ax.set_ylim(0,500)

        ax.set_title("Your Stats", pad = 20)
        plt.tight_layout()
        chart_path = "stats_chart.png"
        plt.savefig(chart_path)
        plt.close()
        print(f"Chart saved → {chart_path}")
        subprocess.run(["xdg-open", chart_path])
    
    def show_stats(self):
        
        print(f"\n{'='*30}")
        print(f"  Level: {self.level}  |  XP: {self.totalXP}")
        print(f"{'='*30}")
        
        for stat, value in self.stats.items():
            print(f"  {stat:<12} {value} XP")
        
        print(f"{'='*30}\n")
        
        self.show_radar()
            


