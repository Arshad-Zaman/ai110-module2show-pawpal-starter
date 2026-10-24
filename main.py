from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner("Arshad")

dog = Pet("Biscuit", "Dog", "Golden Retriever")
cat = Pet("Whiskers", "Cat", "Tabby")
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task("Morning walk", 480, 30, "high", "daily"))
dog.add_task(Task("Evening walk", 1080, 30, "high", "daily"))
cat.add_task(Task("Feeding", 540, 10, "medium", "daily"))

scheduler = Scheduler()
plan = scheduler.generate_plan(owner, available_minutes=90)

print("Today's Schedule:")
print(scheduler.explain_plan(plan))
