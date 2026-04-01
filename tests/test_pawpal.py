import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet


def test_mark_complete_changes_status():
    """mark_complete() should flip is_complete from False to True."""
    task = Task(task_id=1, description="Walk Mochi", duration=30, frequency="daily")

    assert task.is_complete == False  # starts incomplete
    task.mark_complete()
    assert task.is_complete == True   # now complete


def test_add_task_increases_pet_task_count():
    """add_task() should increase the pet's task list by one each call."""
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    task1 = Task(task_id=1, description="Morning walk", duration=30, frequency="daily")
    task2 = Task(task_id=2, description="Evening walk", duration=20, frequency="daily")

    assert len(pet.tasks) == 0  # starts empty
    pet.add_task(task1)
    assert len(pet.tasks) == 1
    pet.add_task(task2)
    assert len(pet.tasks) == 2
