"""Core classes for PawPal+, matching diagrams/uml.mmd."""

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


class Task:
    def __init__(self, description, scheduled_time, duration_minutes, priority, recurrence):
        self.description = description
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.recurrence = recurrence
        self.completed = False
        self.pet = None  # set by Pet.add_task

    def is_recurring(self):
        """Return True if this task repeats rather than being a one-off."""
        return self.recurrence not in (None, "none")

    def conflicts_with(self, other):
        """Return True if this task's time window overlaps another's."""
        if self.scheduled_time is None or other.scheduled_time is None:
            return False
        start, other_start = self.scheduled_time, other.scheduled_time
        end = start + self.duration_minutes
        other_end = other_start + other.duration_minutes
        return start < other_end and other_start < end

    def mark_complete(self):
        """Mark this task as done."""
        self.completed = True

    def __repr__(self):
        return f"Task({self.description!r}, {self.scheduled_time}, {self.priority})"


class Pet:
    def __init__(self, name, species, breed):
        self.name = name
        self.species = species
        self.breed = breed
        self.tasks = []

    def add_task(self, task):
        """Add a task to this pet's list and link the task back to it."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task):
        """Remove a task from this pet's list."""
        self.tasks.remove(task)


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def remove_pet(self, pet):
        """Remove a pet from this owner's list."""
        self.pets.remove(pet)

    def get_all_tasks(self):
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    def generate_plan(self, owner, available_minutes):
        """Build a prioritized, time-limited task plan across all of the owner's pets."""
        tasks = self.sort_by_priority(owner.get_all_tasks())
        return self.filter_by_time(tasks, available_minutes)

    def sort_by_priority(self, tasks):
        """Return tasks ordered from highest to lowest priority."""
        return sorted(tasks, key=lambda t: PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)))

    def filter_by_time(self, tasks, available_minutes):
        """Greedily keep tasks that still fit within the remaining time budget."""
        plan = []
        remaining = available_minutes
        for task in tasks:
            if task.duration_minutes <= remaining:
                plan.append(task)
                remaining -= task.duration_minutes
        return plan

    def explain_plan(self, plan):
        """Return a human-readable summary of the given plan."""
        lines = [
            f"- {task.description} for {task.pet.name} "
            f"({task.duration_minutes} min, {task.priority} priority)"
            for task in plan
        ]
        return "\n".join(lines) if lines else "No tasks fit in the available time."
