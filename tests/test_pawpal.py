import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task, Scheduler


def test_mark_complete_changes_status():
    task = Task("Feeding", 480, 10, "high", "daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    assert len(pet.tasks) == 0

    pet.add_task(Task("Morning walk", 480, 30, "high", "daily"))

    assert len(pet.tasks) == 1


# --- Sorting correctness ---

def test_sort_by_time_returns_chronological_order():
    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    evening = Task("Evening walk", 1080, 30, "high", "daily")
    morning = Task("Morning walk", 480, 30, "high", "daily")
    midday = Task("Lunch", 720, 15, "medium", "daily")
    for task in (evening, morning, midday):
        pet.add_task(task)

    sorted_tasks = Scheduler().sort_by_time(pet.tasks)

    assert sorted_tasks == [morning, midday, evening]


def test_sort_by_time_pushes_unscheduled_tasks_last():
    pet = Pet("Whiskers", "Cat", "Tabby")
    unscheduled = Task("Vet checkup", None, 45, "high", "none")
    scheduled = Task("Feeding", 540, 10, "medium", "daily")
    pet.add_task(unscheduled)
    pet.add_task(scheduled)

    sorted_tasks = Scheduler().sort_by_time(pet.tasks)

    assert sorted_tasks == [scheduled, unscheduled]


def test_sort_by_time_handles_empty_list():
    assert Scheduler().sort_by_time([]) == []


# --- Recurrence logic ---

def test_mark_complete_on_daily_task_schedules_next_day():
    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    task = Task("Morning walk", 480, 30, "high", "daily")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task in pet.tasks
    assert next_task.description == task.description
    assert next_task.scheduled_time == task.scheduled_time
    assert next_task.due_date == task.due_date + timedelta(days=1)
    assert next_task.completed is False


def test_mark_complete_on_weekly_task_schedules_next_week():
    pet = Pet("Clover", "Rabbit", "Holland Lop")
    task = Task("Cage cleaning", 600, 20, "low", "weekly")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.due_date == task.due_date + timedelta(weeks=1)


def test_mark_complete_on_non_recurring_task_schedules_nothing():
    pet = Pet("Whiskers", "Cat", "Tabby")
    task = Task("Vet checkup", 720, 45, "high", "none")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is None
    assert len(pet.tasks) == 1


# --- Conflict detection ---

def test_detect_conflicts_flags_overlapping_tasks_same_time():
    dog = Pet("Biscuit", "Dog", "Golden Retriever")
    cat = Pet("Whiskers", "Cat", "Tabby")
    feeding = Task("Feeding", 540, 10, "medium", "daily")
    grooming = Task("Grooming appointment", 540, 30, "medium", "none")
    dog.add_task(grooming)
    cat.add_task(feeding)

    conflicts = Scheduler().detect_conflicts([feeding, grooming])

    assert len(conflicts) == 1
    assert "Feeding" in conflicts[0]
    assert "Grooming appointment" in conflicts[0]


def test_detect_conflicts_ignores_back_to_back_tasks():
    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    first = Task("Walk", 540, 30, "medium", "none")   # 09:00-09:30
    second = Task("Brushing", 570, 15, "low", "none")  # 09:30-09:45
    pet.add_task(first)
    pet.add_task(second)

    conflicts = Scheduler().detect_conflicts([first, second])

    assert conflicts == []


def test_detect_conflicts_ignores_same_time_on_different_due_dates():
    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    today = Task("Walk", 540, 30, "medium", "none", due_date=date.today())
    tomorrow = Task("Walk", 540, 30, "medium", "none", due_date=date.today() + timedelta(days=1))
    pet.add_task(today)
    pet.add_task(tomorrow)

    conflicts = Scheduler().detect_conflicts([today, tomorrow])

    assert conflicts == []


def test_detect_conflicts_handles_empty_and_single_task_lists():
    assert Scheduler().detect_conflicts([]) == []

    pet = Pet("Biscuit", "Dog", "Golden Retriever")
    task = Task("Walk", 540, 30, "medium", "none")
    pet.add_task(task)

    assert Scheduler().detect_conflicts([task]) == []
