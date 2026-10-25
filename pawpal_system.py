"""Core classes for PawPal+, matching diagrams/uml.mmd."""

from datetime import date, timedelta

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# How far out the next occurrence of a recurring task is due, by recurrence value.
RECURRENCE_DELTA = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


class Task:
    def __init__(self, description, scheduled_time, duration_minutes, priority, recurrence, due_date=None):
        self.description = description
        self.scheduled_time = scheduled_time
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.recurrence = recurrence
        self.completed = False
        self.pet = None  # set by Pet.add_task
        self.due_date = due_date if due_date is not None else date.today()

    def is_recurring(self):
        """Return True if this task repeats rather than being a one-off."""
        return self.recurrence not in (None, "none")

    def conflicts_with(self, other):
        """Return True if this task's time window overlaps another's on the same due_date."""
        if self.scheduled_time is None or other.scheduled_time is None:
            return False
        if self.due_date != other.due_date:
            return False
        start, other_start = self.scheduled_time, other.scheduled_time
        end = start + self.duration_minutes
        other_end = other_start + other.duration_minutes
        return start < other_end and other_start < end

    def mark_complete(self):
        """Mark this task as done.

        If this task recurs ("daily" or "weekly"), automatically schedule
        its next occurrence as a new Task on the same pet, due_date advanced
        by the recurrence interval.
        """
        self.completed = True

        delta = RECURRENCE_DELTA.get(self.recurrence)
        if delta is not None and self.pet is not None:
            next_task = Task(
                self.description,
                self.scheduled_time,
                self.duration_minutes,
                self.priority,
                self.recurrence,
                due_date=self.due_date + delta,
            )
            self.pet.add_task(next_task)
            return next_task
        return None

    def time_str(self):
        """Return scheduled_time formatted as HH:MM, or '--:--' if unset."""
        if self.scheduled_time is None:
            return "--:--"
        hours, minutes = divmod(self.scheduled_time, 60)
        return f"{hours:02d}:{minutes:02d}"

    def __repr__(self):
        return f"Task({self.description!r}, {self.time_str()}, {self.priority}, due={self.due_date})"


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

    def sort_by_time(self, tasks):
        """Return tasks ordered earliest to latest by scheduled_time.

        Tasks with no scheduled_time (None) are sorted last.
        """
        return sorted(
            tasks,
            key=lambda t: t.scheduled_time if t.scheduled_time is not None else float("inf"),
        )

    def detect_conflicts(self, tasks):
        """Return a list of warning strings for any tasks that overlap in time.

        Lightweight pairwise check (reuses Task.conflicts_with) across all
        given tasks, regardless of which pet they belong to -- an owner
        can't be in two places at once, so conflicts across different pets
        matter too. Never raises; just returns warnings for the caller to
        display or act on.
        """
        warnings = []
        for i, task in enumerate(tasks):
            for other in tasks[i + 1:]:
                if task.conflicts_with(other):
                    warnings.append(
                        f"Conflict: '{task.description}' ({task.pet.name}, {task.time_str()}) "
                        f"overlaps with '{other.description}' ({other.pet.name}, {other.time_str()})"
                    )
        return warnings

    def filter_tasks(self, tasks, pet_name=None, completed=None):
        """Return tasks matching the given pet name and/or completion status.

        Either filter can be left as None to skip it.
        """
        return [
            t for t in tasks
            if (pet_name is None or (t.pet is not None and t.pet.name == pet_name))
            and (completed is None or t.completed == completed)
        ]

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
            f"- [{task.time_str()}] {task.description} for {task.pet.name} "
            f"({task.duration_minutes} min, {task.priority} priority)"
            for task in plan
        ]
        return "\n".join(lines) if lines else "No tasks fit in the available time."
