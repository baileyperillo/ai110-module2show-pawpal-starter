from pawpal_system import Task, Pet, Owner, Scheduler
#This is your temporary "testing ground" to 
# verify your logic works in the terminal.

# --- Create Owner ---
owner = Owner(owner_id=1, name="Bailey", email="bailey@email.com")

# --- Create Pets ---
dog = Pet(pet_id=1, name="Mochi", animal_type="dog")
cat = Pet(pet_id=2, name="Luna",  animal_type="cat")

# --- Create Tasks ---
walk      = Task(task_id=1, description="Morning walk",      duration=30,  frequency="daily")
feed_dog  = Task(task_id=2, description="Feed Mochi",        duration=5,   frequency="daily")
feed_cat  = Task(task_id=3, description="Feed Luna",         duration=5,   frequency="daily")
vet_visit = Task(task_id=4, description="Vet check-up",      duration=60,  frequency="monthly")
playtime  = Task(task_id=5, description="Laser pointer play",duration=15,  frequency="daily")

# --- Assign Tasks to Pets ---
dog.tasks = [walk, feed_dog, vet_visit]
cat.tasks = [feed_cat, playtime]

# --- Add Pets to Owner ---
owner.pets = [dog, cat]

# --- Print Today's Schedule ---
scheduler = Scheduler(owner=owner)

print("=" * 40)
print("       PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 40)

for pet in owner.pets:
    print(f"\n{pet.name} ({pet.animal_type})")
    print("-" * 30)
    for task in pet.tasks:
        status = "✓" if task.is_complete else "○"
        print(f"  {status} {task.description:<25} {task.duration} min  [{task.frequency}]")

print("\n" + "=" * 40)
