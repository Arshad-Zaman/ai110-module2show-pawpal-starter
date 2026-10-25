from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Arshad")

dog = Pet("Biscuit", "Dog", "Golden Retriever")
cat = Pet("Whiskers", "Cat", "Tabby")
rabbit = Pet("Clover", "Rabbit", "Holland Lop")
owner.add_pet(dog)
owner.add_pet(cat)
owner.add_pet(rabbit)

# 8 tasks across 3 pets, added out of chronological order on purpose, to test sort_by_time.
dog.add_task(Task("Evening walk", 1080, 30, "high", "daily"))
cat.add_task(Task("Feeding", 540, 10, "medium", "daily"))
rabbit.add_task(Task("Cage cleaning", 600, 20, "low", "weekly"))
dog.add_task(Task("Morning walk", 480, 30, "high", "daily"))
cat.add_task(Task("Vet checkup", 720, 45, "high", "none"))
rabbit.add_task(Task("Evening feeding", 1100, 10, "medium", "daily"))
dog.add_task(Task("Brushing", 1200, 15, "low", "weekly"))
cat.add_task(Task("Litter box cleaning", 660, 10, "medium", "daily"))

scheduler = Scheduler()

# --- Step 1: show the full task list as-is (insertion order) ---
tasks = owner.get_all_tasks()

print("All tasks (unsorted):")
for task in tasks:
    print(f"  {task}")

# --- Step 2: demo sort_by_time ---
sorted_tasks = scheduler.sort_by_time(tasks)

print("\nAll tasks (after sort_by_time):")
for task in sorted_tasks:
    print(f"  {task}")

# --- Step 3: mark some of the (now time-ordered) tasks as done ---
# Morning walk and Feeding are "daily"; Cage cleaning is "weekly" -- marking
# a recurring task complete should auto-schedule its next occurrence.
print("\nMarking tasks as done:")
new_occurrences = []
for task in sorted_tasks:
    if task.description in ("Morning walk", "Cage cleaning", "Feeding"):
        print(f"  {task.description} ({task.pet.name}) -> done")
        next_task = task.mark_complete()
        if next_task is not None:
            new_occurrences.append(next_task)

# --- Step 4: filter the sorted list down to completed tasks only ---
done_tasks = scheduler.filter_tasks(sorted_tasks, completed=True)

print("\nCompleted tasks (filtered from sorted list):")
for task in done_tasks:
    print(f"  {task}")

# --- Step 5: show the next occurrences that were auto-created ---
print("\nNext occurrences auto-scheduled from recurring tasks:")
for task in new_occurrences:
    print(f"  {task.description} ({task.pet.name}) -> {task}")

# --- Step 6: conflict detection demo ---
# Two tasks scheduled at the same time, for different pets, so Arshad
# can't physically do both at once.
dog.add_task(Task("Grooming appointment", 540, 30, "medium", "none"))  # 09:00, overlaps Feeding
conflicts = scheduler.detect_conflicts(owner.get_all_tasks())

print("\nConflict check:")
if conflicts:
    for warning in conflicts:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts found.")
