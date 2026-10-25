# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🛠️ Implementation Summary

I built four classes in `pawpal_system.py`: Owner, Pet, Task, and Scheduler.

An Owner holds a list of Pets and can get every task across all of them with `get_all_tasks()`. A Pet holds its own list of Tasks and can add or remove them. A Task stores its description, scheduled time, duration, priority, recurrence, and completion status, and can check for time conflicts with another task.

The Scheduler is the brain. It calls `owner.get_all_tasks()` to pull tasks from every pet at once, sorts them by priority, then fills a time budget greedily, keeping tasks until the available minutes run out. `explain_plan()` turns the result into a readable "Today's Schedule" list. `main.py` wires this together and prints that schedule to the terminal.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
$ python main.py
Today's Schedule:
- Morning walk for Biscuit (30 min, high priority)
- Evening walk for Biscuit (30 min, high priority)
- Feeding for Whiskers (10 min, medium priority)
```

## 🧪 Testing PawPal+

Run the full suite from the project root with:

```bash
python -m pytest
```

`tests/test_pawpal.py` covers the core behaviors the scheduler depends on:

- **Sorting correctness** — `sort_by_time()` returns tasks in chronological order, pushes tasks with no `scheduled_time` to the end, and handles an empty list without error.
- **Recurrence logic** — marking a `daily` task complete with `mark_complete()` schedules its next occurrence one day later, a `weekly` task schedules one week later, and a `none` task schedules nothing.
- **Conflict detection** — `detect_conflicts()` flags two tasks that overlap at the same time across different pets, but correctly leaves back-to-back tasks (one ending exactly when the next starts) and same-time tasks on different `due_date`s unflagged.
- A couple of baseline checks on `Task.mark_complete()` and `Pet.add_task()` from earlier in the project.

Sample test output:

```
$ python -m pytest -v
============================= test session starts ==============================
platform linux -- Python 3.12.3, pytest-9.1.1, pluggy-1.7.0
rootdir: /home/rizz/Documents/AI110/ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 12 items

tests/test_pawpal.py::test_mark_complete_changes_status PASSED           [  8%]
tests/test_pawpal.py::test_add_task_increases_pet_task_count PASSED      [ 16%]
tests/test_pawpal.py::test_sort_by_time_returns_chronological_order PASSED [ 25%]
tests/test_pawpal.py::test_sort_by_time_pushes_unscheduled_tasks_last PASSED [ 33%]
tests/test_pawpal.py::test_sort_by_time_handles_empty_list PASSED        [ 41%]
tests/test_pawpal.py::test_mark_complete_on_daily_task_schedules_next_day PASSED [ 50%]
tests/test_pawpal.py::test_mark_complete_on_weekly_task_schedules_next_week PASSED [ 58%]
tests/test_pawpal.py::test_mark_complete_on_non_recurring_task_schedules_nothing PASSED [ 66%]
tests/test_pawpal.py::test_detect_conflicts_flags_overlapping_tasks_same_time PASSED [ 75%]
tests/test_pawpal.py::test_detect_conflicts_ignores_back_to_back_tasks PASSED [ 83%]
tests/test_pawpal.py::test_detect_conflicts_ignores_same_time_on_different_due_dates PASSED [ 91%]
tests/test_pawpal.py::test_detect_conflicts_handles_empty_and_single_task_lists PASSED [100%]

============================== 12 passed in 0.02s ==============================
```

**Confidence Level: ⭐⭐⭐⭐☆ (4/5)**

All 12 tests pass, and they cover the three behaviors I was least sure about going in: whether sorting handles unscheduled tasks correctly, whether recurrence actually advances the due date by the right interval, and whether conflict detection respects day boundaries instead of just comparing raw times. I'm not at 5 stars because the suite only exercises `Scheduler` and `Task`/`Pet` in isolation — `generate_plan()` (the method that chains priority sorting with the time-budget filter) and the Streamlit UI in `app.py` aren't covered yet, so I can't be fully confident in how those pieces behave together.

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | Sorts by scheduled time (earliest first) or priority (high to low) |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name, completion status, or both at once |
| Conflict handling | `Scheduler.detect_conflicts()`, `Task.conflicts_with()` | Flags overlapping time slots across all pets, same day |
| Recurring tasks | `Task.mark_complete()` | Auto-schedules the next occurrence for daily/weekly tasks |

**Task sorting.** `Scheduler.sort_by_time()` orders tasks earliest to latest using `scheduled_time`, pushing anything with no time set to the end. `sort_by_priority()` orders high to low priority. Neither one mutates the original list — both return a new sorted list, so calling them doesn't change `pet.tasks` or `owner.get_all_tasks()`.

**Filtering.** `Scheduler.filter_tasks(tasks, pet_name=None, completed=None)` returns only the tasks matching whichever filters you pass in. Leave `pet_name` or `completed` as `None` to skip that filter, or use both together to, say, get one pet's incomplete tasks in a single call.

**Conflict handling.** `Task.conflicts_with(other)` checks if two tasks overlap in time on the same `due_date`. `Scheduler.detect_conflicts(tasks)` runs that check pairwise across every task passed in, regardless of which pet they belong to, since one owner can't physically do two things at once. It never raises — it just returns a list of warning strings for the caller to print or act on.

**Recurring tasks.** Tasks have a `recurrence` field ("daily", "weekly", or "none") and a `due_date`. When `Task.mark_complete()` is called on a recurring task, it marks the task done and automatically creates the next occurrence as a new `Task` on the same pet, with `due_date` advanced by a day (daily) or a week (weekly), using `datetime.timedelta`.

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
