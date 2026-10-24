import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pawpal_system import Pet, Task


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
