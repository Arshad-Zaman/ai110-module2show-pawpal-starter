"""Class stubs for PawPal+, matching diagrams/uml.mmd. No logic yet."""


class Owner:
    def __init__(self, name):
        self.name = name
        self.pets = []

    def add_pet(self, pet):
        pass

    def remove_pet(self, pet):
        pass


class Pet:
    def __init__(self, name, species, breed):
        self.name = name
        self.species = species
        self.breed = breed
        self.tasks = []

    def add_task(self, task):
        pass

    def remove_task(self, task):
        pass


class Task:
    def __init__(self, name, category, duration_minutes, priority, recurrence):
        self.name = name
        self.category = category
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.recurrence = recurrence

    def is_recurring(self):
        pass

    def conflicts_with(self, other):
        pass


class Scheduler:
    def generate_plan(self, pet, available_minutes):
        pass

    def sort_by_priority(self, tasks):
        pass

    def filter_by_time(self, tasks, available_minutes):
        pass

    def explain_plan(self, plan):
        pass
