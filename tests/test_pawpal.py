import sys
import os
from datetime import datetime, timedelta
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, Owner, Scheduler


# =========================================================================
# EXISTING TESTS - PRESERVE
# =========================================================================

def test_mark_complete_changes_status():
    """mark_complete() should flip is_complete from False to True."""
    task = Task(task_id=1, description="Walk Mochi", duration=30, frequency="daily")
    assert task.is_complete == False
    task.mark_complete()
    assert task.is_complete == True


def test_add_task_increases_pet_task_count():
    """add_task() should increase the pet's task list by one each call."""
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    task1 = Task(task_id=1, description="Morning walk", duration=30, frequency="daily")
    task2 = Task(task_id=2, description="Evening walk", duration=20, frequency="daily")
    assert len(pet.tasks) == 0
    pet.add_task(task1)
    assert len(pet.tasks) == 1
    pet.add_task(task2)
    assert len(pet.tasks) == 2


# =========================================================================
# SORTING TESTS - Sort by duration, time, and frequency
# =========================================================================

def test_sort_by_duration_happy_path():
    """sort_tasks_by_duration() should sort multiple tasks from shortest to longest."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Quick brush", duration=15, frequency="daily")
    task2 = Task(task_id=2, description="Full walk", duration=45, frequency="daily")
    task3 = Task(task_id=3, description="Medium play", duration=30, frequency="daily")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_duration()
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].duration == 15
    assert sorted_tasks[1].duration == 30
    assert sorted_tasks[2].duration == 45


def test_sort_by_duration_all_same():
    """sort_tasks_by_duration() should handle tasks with identical durations without crashing."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Task A", duration=20, frequency="daily")
    task2 = Task(task_id=2, description="Task B", duration=20, frequency="daily")
    task3 = Task(task_id=3, description="Task C", duration=20, frequency="daily")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_duration()
    
    assert len(sorted_tasks) == 3
    assert all(task.duration == 20 for task in sorted_tasks)


def test_sort_by_duration_empty_list():
    """sort_tasks_by_duration() should return empty list when owner has no pets."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    scheduler = Scheduler(owner=owner)
    
    sorted_tasks = scheduler.sort_tasks_by_duration()
    
    assert sorted_tasks == []


def test_sort_by_time_happy_path():
    """sort_by_time() should sort tasks chronologically by HH:MM time format."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Evening walk", duration=30, frequency="daily", time="18:00")
    task2 = Task(task_id=2, description="Morning walk", duration=30, frequency="daily", time="09:00")
    task3 = Task(task_id=3, description="Afternoon play", duration=30, frequency="daily", time="14:30")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].time == "09:00"
    assert sorted_tasks[1].time == "14:30"
    assert sorted_tasks[2].time == "18:00"


def test_sort_by_time_midnight_boundaries():
    """sort_by_time() should correctly handle 00:00 and 23:59 times."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Late night", duration=20, frequency="daily", time="23:59")
    task2 = Task(task_id=2, description="Midnight", duration=20, frequency="daily", time="00:00")
    task3 = Task(task_id=3, description="Noon", duration=20, frequency="daily", time="12:00")
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_by_time()
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].time == "00:00"
    assert sorted_tasks[1].time == "12:00"
    assert sorted_tasks[2].time == "23:59"


def test_sort_by_frequency_happy_path():
    """sort_tasks_by_frequency() should group by frequency then sort by due_date."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 1)
    task1 = Task(task_id=1, description="Weekly task", duration=30, frequency="weekly", 
                 due_date=base_date + timedelta(days=7))
    task2 = Task(task_id=2, description="Daily task 1", duration=30, frequency="daily", 
                 due_date=base_date)
    task3 = Task(task_id=3, description="Daily task 2", duration=30, frequency="daily", 
                 due_date=base_date + timedelta(days=1))
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_frequency()
    
    assert len(sorted_tasks) == 3
    # First two should be daily (sorted by date), then weekly
    assert sorted_tasks[0].frequency == "daily"
    assert sorted_tasks[1].frequency == "daily"
    assert sorted_tasks[2].frequency == "weekly"
    # Within daily frequency, should be sorted by due date
    assert sorted_tasks[0].due_date <= sorted_tasks[1].due_date


def test_sort_by_frequency_all_same():
    """sort_tasks_by_frequency() should sort by due_date when all have same frequency."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 1)
    task1 = Task(task_id=1, description="Task 1", duration=20, frequency="daily",
                 due_date=base_date + timedelta(days=2))
    task2 = Task(task_id=2, description="Task 2", duration=20, frequency="daily",
                 due_date=base_date)
    task3 = Task(task_id=3, description="Task 3", duration=20, frequency="daily",
                 due_date=base_date + timedelta(days=1))
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    sorted_tasks = scheduler.sort_tasks_by_frequency()
    
    assert len(sorted_tasks) == 3
    assert sorted_tasks[0].due_date == base_date
    assert sorted_tasks[1].due_date == base_date + timedelta(days=1)
    assert sorted_tasks[2].due_date == base_date + timedelta(days=2)


# =========================================================================
# RECURRENCE TESTS - Test recurring task logic and task generation
# =========================================================================

def test_daily_recurrence_creates_next_task():
    """complete_task_with_recurrence() should create a new task 1 day later for daily tasks."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15, 9, 0)
    task = Task(task_id=1, description="Daily walk", duration=30, frequency="daily",
                due_date=base_date)
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.due_date == base_date + timedelta(days=1)
    assert task.is_complete == True
    assert len(pet.tasks) == 2


def test_weekly_recurrence_creates_next_task():
    """complete_task_with_recurrence() should create a new task 7 days later for weekly tasks."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15, 10, 0)
    task = Task(task_id=1, description="Weekly bath", duration=60, frequency="weekly",
                due_date=base_date)
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task is not None
    assert next_task.frequency == "weekly"
    assert next_task.due_date == base_date + timedelta(days=7)
    assert task.is_complete == True
    assert len(pet.tasks) == 2


def test_one_time_task_no_recurrence():
    """complete_task_with_recurrence() should return None for one-time tasks."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=1, description="Vet appointment", duration=45, frequency="one-time",
                due_date=datetime(2026, 4, 20))
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task is None
    assert task.is_complete == True
    assert len(pet.tasks) == 1  # No new task created


def test_recurrence_preserves_task_properties():
    """Recurring task should preserve description, duration, and priority."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=1, description="Morning kibble", duration=5, frequency="daily",
                priority="high", time="08:00", due_date=datetime(2026, 4, 15))
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task.description == "Morning kibble"
    assert next_task.duration == 5
    assert next_task.priority == "high"
    assert next_task.time == "08:00"
    assert next_task.frequency == "daily"


def test_recurrence_month_boundary():
    """Daily task on 4/30 should create new task on 5/1 correctly."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=1, description="Daily task", duration=20, frequency="daily",
                due_date=datetime(2026, 4, 30))
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task.due_date == datetime(2026, 5, 1)
    assert next_task.due_date.day == 1
    assert next_task.due_date.month == 5


def test_recurrence_year_boundary():
    """Task on 12/31 should create new task on 1/1 of next year correctly."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=1, description="New Year task", duration=20, frequency="daily",
                due_date=datetime(2025, 12, 31))
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task.due_date == datetime(2026, 1, 1)
    assert next_task.due_date.year == 2026
    assert next_task.due_date.month == 1
    assert next_task.due_date.day == 1


def test_recurrence_task_id_unique():
    """Each recurrence should have a unique task_id (original + 1000)."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=5, description="Daily task", duration=20, frequency="daily",
                due_date=datetime(2026, 4, 15))
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    next_task = scheduler.complete_task_with_recurrence(task, pet)
    
    assert next_task.task_id == task.task_id + 1000
    assert next_task.task_id == 1005
    assert next_task.task_id != task.task_id


# =========================================================================
# CONFLICT DETECTION TESTS - Verify scheduling conflict detection
# =========================================================================

def test_detect_conflict_two_tasks_same_time():
    """detect_scheduling_conflicts() should flag two tasks at same date/time."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15)
    task1 = Task(task_id=1, description="Morning walk", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    task2 = Task(task_id=2, description="Morning training", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) > 0
    assert any("CONFLICT" in warning for warning in warnings)


def test_detect_conflict_multiple_conflicts():
    """detect_scheduling_conflicts() should detect multiple conflicts at different times."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15)
    
    # First conflict: two tasks at 09:00
    task1 = Task(task_id=1, description="Walk 1", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    task2 = Task(task_id=2, description="Walk 2", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    
    # Second conflict: two tasks at 14:00
    task3 = Task(task_id=3, description="Play 1", duration=30, frequency="daily",
                 time="14:00", due_date=base_date)
    task4 = Task(task_id=4, description="Play 2", duration=30, frequency="daily",
                 time="14:00", due_date=base_date)
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    pet.add_task(task4)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) >= 2
    assert all("CONFLICT" in warning for warning in warnings)


def test_detect_no_conflict_different_times():
    """detect_scheduling_conflicts() should return no warnings when all times different."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15)
    task1 = Task(task_id=1, description="Morning walk", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    task2 = Task(task_id=2, description="Afternoon play", duration=30, frequency="daily",
                 time="14:00", due_date=base_date)
    task3 = Task(task_id=3, description="Evening walk", duration=30, frequency="daily",
                 time="18:00", due_date=base_date)
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) == 0


def test_detect_conflict_across_pets():
    """detect_scheduling_conflicts() should flag conflicts across different pets."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet1 = Pet(pet_id=1, name="Mochi", animal_type="dog")
    pet2 = Pet(pet_id=2, name="Whiskers", animal_type="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    base_date = datetime(2026, 4, 15)
    task1 = Task(task_id=1, description="Dog walk", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    task2 = Task(task_id=2, description="Cat feeding", duration=10, frequency="daily",
                 time="09:00", due_date=base_date)
    
    pet1.add_task(task1)
    pet2.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) > 0
    assert any("CONFLICT" in warning for warning in warnings)
    assert any("Mochi" in warning or "Whiskers" in warning for warning in warnings)


def test_detect_conflict_different_dates_no_conflict():
    """detect_scheduling_conflicts() should not flag tasks at same time on different dates."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Walk day 1", duration=30, frequency="daily",
                 time="09:00", due_date=datetime(2026, 4, 15))
    task2 = Task(task_id=2, description="Walk day 2", duration=30, frequency="daily",
                 time="09:00", due_date=datetime(2026, 4, 16))
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) == 0


def test_detect_conflict_returns_warning_messages():
    """Conflict warnings should contain date, time, pet names, and task descriptions."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    base_date = datetime(2026, 4, 15)
    task1 = Task(task_id=1, description="Morning walk", duration=30, frequency="daily",
                 time="09:00", due_date=base_date)
    task2 = Task(task_id=2, description="Morning kibble", duration=10, frequency="daily",
                 time="09:00", due_date=base_date)
    
    pet.add_task(task1)
    pet.add_task(task2)
    
    scheduler = Scheduler(owner=owner)
    warnings = scheduler.detect_scheduling_conflicts()
    
    assert len(warnings) > 0
    warning_text = " ".join(warnings)
    
    # Should contain date, time, pet name, and descriptions
    assert "2026-04-15" in warning_text
    assert "09:00" in warning_text
    assert "Mochi" in warning_text
    assert "Morning walk" in warning_text
    assert "Morning kibble" in warning_text


# =========================================================================
# FILTER & EMPTY DATA TESTS - Test filtering and empty collections
# =========================================================================

def test_empty_pet_no_tasks():
    """Pet with no tasks should return empty list from get_tasks()."""
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    
    tasks = pet.get_tasks()
    
    assert tasks == []
    assert len(tasks) == 0


def test_empty_owner_no_pets():
    """Owner with no pets should return empty list from get_all_tasks()."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    
    all_tasks = owner.get_all_tasks()
    
    assert all_tasks == []
    assert len(all_tasks) == 0


def test_filter_by_pet_name_exists():
    """filter_by_pet_name() should return only tasks for the specified pet."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet1 = Pet(pet_id=1, name="Mochi", animal_type="dog")
    pet2 = Pet(pet_id=2, name="Whiskers", animal_type="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task(task_id=1, description="Dog walk", duration=30, frequency="daily")
    task2 = Task(task_id=2, description="Dog feed", duration=10, frequency="daily")
    task3 = Task(task_id=3, description="Cat feed", duration=10, frequency="daily")
    
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    mochi_tasks = scheduler.filter_by_pet_name("Mochi")
    
    assert len(mochi_tasks) == 2
    assert all("Dog" in task.description for task in mochi_tasks)


def test_filter_by_pet_name_not_exists():
    """filter_by_pet_name() should return empty list for nonexistent pet."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task = Task(task_id=1, description="Walk", duration=30, frequency="daily")
    pet.add_task(task)
    
    scheduler = Scheduler(owner=owner)
    nonexistent_tasks = scheduler.filter_by_pet_name("Fluffy")
    
    assert nonexistent_tasks == []


def test_filter_by_completion_status():
    """filter_by_completion_status() should separate complete and pending tasks."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet = Pet(pet_id=1, name="Mochi", animal_type="dog")
    owner.add_pet(pet)
    
    task1 = Task(task_id=1, description="Completed walk", duration=30, frequency="daily",
                 is_complete=True)
    task2 = Task(task_id=2, description="Pending walk", duration=30, frequency="daily",
                 is_complete=False)
    task3 = Task(task_id=3, description="Completed feed", duration=10, frequency="daily",
                 is_complete=True)
    
    pet.add_task(task1)
    pet.add_task(task2)
    pet.add_task(task3)
    
    scheduler = Scheduler(owner=owner)
    completed = scheduler.filter_by_completion_status(True)
    pending = scheduler.filter_by_completion_status(False)
    
    assert len(completed) == 2
    assert len(pending) == 1
    assert all(task.is_complete for task in completed)
    assert all(not task.is_complete for task in pending)


def test_filter_combined_completion_and_pet():
    """filter_tasks() should filter by both completion status and pet name."""
    owner = Owner(owner_id=1, name="Bailey", email="bailey@example.com")
    pet1 = Pet(pet_id=1, name="Mochi", animal_type="dog")
    pet2 = Pet(pet_id=2, name="Whiskers", animal_type="cat")
    owner.add_pet(pet1)
    owner.add_pet(pet2)
    
    task1 = Task(task_id=1, description="Dog walk", duration=30, frequency="daily",
                 is_complete=True)
    task2 = Task(task_id=2, description="Dog feed", duration=10, frequency="daily",
                 is_complete=False)
    task3 = Task(task_id=3, description="Cat feed", duration=10, frequency="daily",
                 is_complete=True)
    task4 = Task(task_id=4, description="Cat play", duration=20, frequency="daily",
                 is_complete=False)
    
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)
    
    scheduler = Scheduler(owner=owner)
    
    # Filter: Mochi's tasks that are complete
    mochi_complete = scheduler.filter_tasks(is_complete=True, pet_name="Mochi")
    
    # Filter: Whiskers' tasks that are pending
    whiskers_pending = scheduler.filter_tasks(is_complete=False, pet_name="Whiskers")
    
    assert len(mochi_complete) == 1
    assert mochi_complete[0].description == "Dog walk"
    
    assert len(whiskers_pending) == 1
    assert whiskers_pending[0].description == "Cat play"
