# This will be your "logic layer" where 
# all your backend classes live.
#Created by CoPilot
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime


@dataclass
class OwnerInfo:
    """Stores owner's personal information and pet count."""
    owner_id: int
    name: str
    email: str
    phone: str
    number_of_pets: int = 0
    
    def add_owner_info(self) -> None:
        """Add owner information to the system."""
        # Validate required fields
        if not self.name or not self.email or not self.phone:
            raise ValueError("Name, email, and phone are required")
        # Basic email validation
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        if self.number_of_pets < 0:
            raise ValueError("Number of pets cannot be negative")
        # In a real system, this would save to database
        print(f"Owner '{self.name}' added successfully")
    
    def edit_owner_info(self) -> None:
        """Edit the owner's information."""
        # Validate required fields
        if not self.name or not self.email or not self.phone:
            raise ValueError("Name, email, and phone are required")
        # Basic email validation
        if "@" not in self.email:
            raise ValueError("Invalid email format")
        if self.number_of_pets < 0:
            raise ValueError("Number of pets cannot be negative")
        # In a real system, this would update in database
        print(f"Owner '{self.name}' updated successfully")


@dataclass
class PetInfo:
    """Stores individual pet information and metadata."""
    pet_id: int
    owner_id: int
    pet_name: str
    animal_type: str
    breed: Optional[str] = None
    age: Optional[int] = None
    
    def add_pet(self) -> None:
        """Add a new pet to the system."""
        # Validate required fields
        if not self.pet_name or not self.animal_type:
            raise ValueError("Pet name and animal type are required")
        if self.age is not None and self.age < 0:
            raise ValueError("Age cannot be negative")
        # In a real system, this would save to database
        print(f"Pet '{self.pet_name}' added successfully")
    
    def edit_pet(self) -> None:
        """Edit the pet's information."""
        # Validate required fields
        if not self.pet_name or not self.animal_type:
            raise ValueError("Pet name and animal type are required")
        if self.age is not None and self.age < 0:
            raise ValueError("Age cannot be negative")
        # In a real system, this would update in database
        print(f"Pet '{self.pet_name}' updated successfully")


@dataclass
class Task:
    """Stores individual task/activity information."""
    task_id: int
    owner_id: int
    task_name: str
    duration: int  # in minutes
    priority: int  # 1-5 or similar scale
    created_at: datetime = field(default_factory=datetime.now)
    assigned_pet: Optional[PetInfo] = None
    
    def create_task(self) -> None:
        """Create a new task."""
        # Validate required fields
        if not self.task_name:
            raise ValueError("Task name is required")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not (1 <= self.priority <= 5):
            raise ValueError("Priority must be between 1 and 5")
        # In a real system, this would save to database
        print(f"Task '{self.task_name}' created successfully")
    
    def edit_task(self) -> None:
        """Edit the task's information."""
        # Validate required fields
        if not self.task_name:
            raise ValueError("Task name is required")
        if self.duration <= 0:
            raise ValueError("Duration must be positive")
        if not (1 <= self.priority <= 5):
            raise ValueError("Priority must be between 1 and 5")
        # In a real system, this would update in database
        print(f"Task '{self.task_name}' updated successfully")
    
    def delete_task(self) -> None:
        """Delete the task."""
        # In a real system, this would remove from database
        print(f"Task '{self.task_name}' deleted successfully")


@dataclass
class TaskList:
    """Organizes and displays tasks, filtered by priority or chronological order."""
    list_id: int
    owner_id: int
    list_name: str
    sort_by: str  # "priority" or "createdDate"
    tasks: List[Task] = field(default_factory=list)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the list."""
        if task.owner_id != self.owner_id:
            raise ValueError("Task must belong to the same owner as the list")
        if task not in self.tasks:
            self.tasks.append(task)
            print(f"Task '{task.task_name}' added to list '{self.list_name}'")
        else:
            print(f"Task '{task.task_name}' is already in the list")
    
    def remove_task(self, task: Task) -> None:
        """Remove a task from the list."""
        if task in self.tasks:
            self.tasks.remove(task)
            print(f"Task '{task.task_name}' removed from list '{self.list_name}'")
        else:
            print(f"Task '{task.task_name}' not found in the list")
    
    def get_tasks(self) -> List[Task]:
        """Get all tasks in the list, sorted by priority or date."""
        if self.sort_by == "priority":
            return sorted(self.tasks, key=lambda t: t.priority)
        elif self.sort_by == "createdDate":
            return sorted(self.tasks, key=lambda t: t.created_at)
        else:
            # Default to priority if invalid sort_by
            return sorted(self.tasks, key=lambda t: t.priority)
    
    def update_sort_order(self, sort_by: str) -> None:
        """Update the sort order (priority or createdDate)."""
        if sort_by not in ["priority", "createdDate"]:
            raise ValueError("Sort order must be 'priority' or 'createdDate'")
        self.sort_by = sort_by
        print(f"Sort order updated to '{sort_by}' for list '{self.list_name}'")


# -----------------------------------------------------------------------
# The following skeleton code was generated by Claude (Anthropic AI).
# Note: Claude reads and considers all existing code before making edits
# or additions, so that new code fits the project's existing structure.
# -----------------------------------------------------------------------

# @dataclass
# class PetInfo:
#     """Stores individual pet information and metadata."""
#     pet_id: int           # unique identifier for each pet
#     pet_name: str         # name of the pet
#     animal_type: str      # e.g. "dog", "cat", "bird"
#     breed: Optional[str] = None   # optional breed info
#     age: Optional[int] = None     # optional age in years
#
#     def enter_pet_info(self) -> None:
#         """Enter a new pet's information into the system."""
#         pass
#
#     def edit_pet_info(self) -> None:
#         """Edit this pet's existing information."""
#         pass


# @dataclass
# class Task:
#     """Stores individual task/activity information."""
#     task_id: int            # unique identifier for each task
#     task_name: str          # e.g. "Walk the dog"
#     duration: int           # estimated time to complete, in minutes
#     priority: str           # "high", "medium", or "low"
#     date_added: datetime = field(default_factory=datetime.now)  # auto-set on creation
#     assigned_pet: Optional[PetInfo] = None  # optionally link task to a specific pet
#
#     def create_task(self) -> None:
#         """Create a new task and add it to the system."""
#         pass
#
#     def edit_task(self) -> None:
#         """Edit this task's information."""
#         pass
#
#     def delete_task(self) -> None:
#         """Delete this task from the system."""
#         pass


# @dataclass
# class TaskList:
#     """Organizes and displays tasks sorted by priority or input order."""
#     tasks: List[Task] = field(default_factory=list)  # starts as an empty list
#
#     def add_task(self, task: Task) -> None:
#         """Add a task to the list."""
#         pass
#
#     def remove_task(self, task: Task) -> None:
#         """Remove a task from the list."""
#         pass
#
#     def sort_by_priority(self) -> List[Task]:
#         """Return tasks sorted by priority: high -> medium -> low."""
#         pass
#
#     def sort_by_date_added(self) -> List[Task]:
#         """Return tasks in the order they were originally added."""
#         pass
#
#     def display_list(self) -> None:
#         """Print all tasks currently in the list."""
#         pass


# @dataclass
# class OwnerInfo:
#     """Stores owner personal info, their pets, and their task list."""
#     owner_id: int           # unique identifier for the owner
#     owner_name: str         # full name of the owner
#     email: str              # owner's email address
#     phone: str              # owner's phone number
#     pets: List[PetInfo] = field(default_factory=list)        # list of owner's pets
#     task_list: TaskList = field(default_factory=TaskList)    # owner's task list
#
#     @property
#     def number_of_pets(self) -> int:
#         """Derived from the pets list — stays accurate without manual tracking."""
#         return len(self.pets)
#
#     def enter_info(self) -> None:
#         """Enter the owner's personal information into the system."""
#         pass
#
#     def edit_info(self) -> None:
#         """Edit the owner's existing personal information."""
#         pass
#
#     def add_pet(self, pet: PetInfo) -> None:
#         """Add a pet to this owner's pet list."""
#         pass
#
#     def remove_pet(self, pet: PetInfo) -> None:
#         """Remove a pet from this owner's pet list."""
#         pass
