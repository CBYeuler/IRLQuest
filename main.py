#!/usr/bin/env python3

import questionary
from engine import User
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def character_creation(user):
    clear()
    print("=" * 40)
    print("  WELCOME TO YOUR JOURNEY")
    print("=" * 40)

    name = questionary.text("\n  Enter your name, traveler:").ask().strip()
    while not name:
        name = questionary.text("  Name cannot be empty:").ask().strip()

    classes = {
        "Warrior":   {"Strength": 50, "Discipline": 50},
        "Scholar":   {"Mind": 50, "Skill": 50},
        "Monk":      {"Faith": 50, "Discipline": 50},
        "Socialite": {"Social": 50, "Mind": 50},
        "Hacker":    {"Skill": 50, "Mind": 50},
        "Ascetic":   {"Faith": 50, "Strength": 50},
    }

    chosen_class = questionary.select(
        "  Choose your class:",
        choices=[
            f"{cls}  (+{list(bonuses.keys())[0]}, +{list(bonuses.keys())[1]})"
            for cls, bonuses in classes.items()
        ]
    ).ask()

    # Extract just the class name from the choice string
    chosen_class_key = chosen_class.split("  ")[0]
    bonuses = classes[chosen_class_key]

    for stat, value in bonuses.items():
        user.stats[stat] += value

    motto = questionary.text(
        "  Enter your motto (or press Enter to skip):"
    ).ask().strip()
    if not motto:
        motto = "The journey is the reward."

    user.name = chosen_class_key
    user.name = name
    user.player_class = chosen_class_key
    user.motto = motto
    user.save()

    clear()
    print(f"\n  Welcome, {name} the {chosen_class_key}.")
    print(f"  \"{motto}\"")
    print(f"\n  Your journey begins.\n")
    input("  Press Enter to continue...")

def show_menu(user):
    clear()
    print(f"\n  ⚔  {user.name} the {user.player_class}  |  Level {user.level}  |  {user.totalXP} XP")
    print(f"  \"{user.motto}\"")
    print()

    return questionary.select(
        "  What will you do?",
        choices=[
            "📋  List tasks",
            "➕  Add task",
            "✅  Complete task",
            "📊  Show stats",
            "❌  Quit"
        ]
    ).ask()

def list_tasks(user):
    clear()
    print("\n  YOUR TASKS\n")
    if not user.tasks:
        print("  No tasks yet.")
    else:
        for t in user.tasks:
            status = "✅" if t["completed"] else "⬜"
            print(f"  {status} [{t['id']}] {t['name']}  +{t['xp']} XP  ({t['stat']})")
    print()
    input("  Press Enter to go back...")

def add_task_flow(user):
    clear()
    print("\n  ADD A TASK\n")

    name = questionary.text("  Task name:").ask().strip()
    while not name:
        name = questionary.text("  Name cannot be empty:").ask().strip()

    while True:
        try:
            xp = int(questionary.text("  XP reward (e.g. 30, 50, 100):").ask())
            if xp <= 0:
                raise ValueError
            break
        except ValueError:
            print("  Please enter a positive number.")

    stat = questionary.select(
        "  Which stat does this task train?",
        choices=["Strength", "Discipline", "Mind", "Faith", "Social", "Skill"]
    ).ask()

    user.add_task(name, xp, stat)
    print(f"\n  Task '{name}' added! → {stat} +{xp} XP")
    input("\n  Press Enter to go back...")

def complete_task_flow(user):
    clear()
    print("\n  COMPLETE A TASK\n")

    incomplete = [t for t in user.tasks if not t["completed"]]
    if not incomplete:
        print("  No incomplete tasks.")
        input("\n  Press Enter to go back...")
        return

    choices = [
        f"[{t['id']}] {t['name']}  +{t['xp']} XP  ({t['stat']})"
        for t in incomplete
    ]

    selected = questionary.select(
        "  Select a task to complete:",
        choices=choices
    ).ask()

    # Match selection back to task by ID
    selected_id = int(selected.split("]")[0].replace("[", ""))
    task = next(t for t in incomplete if t["id"] == selected_id)

    user.complete_task(task["id"])
    print(f"\n  ✅ '{task['name']}' done!  +{task['xp']} XP → {task['stat']}")
    print(f"  Level: {user.level}  |  Total XP: {user.totalXP}")
    input("\n  Press Enter to go back...")

def main():
    user = User()

    try:
        user.load()
    except (FileNotFoundError, KeyError):
        character_creation(user)

    if not hasattr(user, 'name') or not user.name:
        character_creation(user)

    while True:
        choice = show_menu(user)

        if "List" in choice:
            list_tasks(user)
        elif "Add" in choice:
            add_task_flow(user)
        elif "Complete" in choice:
            complete_task_flow(user)
        elif "stats" in choice.lower():
            user.show_stats()
        elif "Quit" in choice:
            clear()
            print(f"\n  Until next time, {user.name}.\n")
            break

if __name__ == "__main__":
    main()
