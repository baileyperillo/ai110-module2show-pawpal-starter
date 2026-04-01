from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import datetime

#This is your temporary "testing ground" to 
# verify your logic works in the terminal.

# --- Create Owner ---
owner = Owner(owner_id=1, name="Bailey", email="bailey@email.com")

# --- Create Pets ---
dog = Pet(pet_id=1, name="Mochi", animal_type="dog")
cat = Pet(pet_id=2, name="Luna",  animal_type="cat")

# --- Create Tasks ---
# Setting same time (14:00) to test conflict detection
today = datetime.now()

walk      = Task(task_id=1, description="Morning walk",       duration=30,  frequency="daily",   priority="high", time="14:00", due_date=today)
feed_dog  = Task(task_id=2, description="Feed Mochi",         duration=5,   frequency="daily",   priority="high", time="09:00", due_date=today)
feed_cat  = Task(task_id=3, description="Feed Luna",          duration=5,   frequency="daily",   priority="high", time="14:00", due_date=today)  # CONFLICT: same time as walk
vet_visit = Task(task_id=4, description="Vet check-up",       duration=60,  frequency="monthly", priority="medium", time="10:00", due_date=today)
playtime  = Task(task_id=5, description="Laser pointer play", duration=15,  frequency="daily",   priority="low", time="15:00", due_date=today)

# --- Assign Tasks to Pets ---
dog.tasks = [walk, feed_dog, vet_visit]
cat.tasks = [feed_cat, playtime]

# --- Add Pets to Owner ---
owner.pets = [dog, cat]

# --- Create Scheduler ---
scheduler = Scheduler(owner=owner)

print("=" * 50)
print("       PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 50)

for pet in owner.pets:
    print(f"\n{pet.name} ({pet.animal_type})")
    print("-" * 45)
    for task in pet.tasks:
        status = "✓" if task.is_complete else "○"
        print(f"  {status} {task.description:<25} {task.duration:2d} min  [{task.time}]  priority: {task.priority}")

print("\n" + "=" * 50)

# --- CONFLICT DETECTION TEST ---
print("\n🔍 CHECKING FOR SCHEDULING CONFLICTS...\n")
conflicts = scheduler.detect_scheduling_conflicts()

if conflicts:
    print("⚠️  CONFLICTS FOUND:\n")
    for warning in conflicts:
        print(warning)
        print()
else:
    print("✅ No conflicts detected!")

print("=" * 50)
