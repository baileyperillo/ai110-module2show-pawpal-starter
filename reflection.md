# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three things user should be able to do:
1. user should enter info on themselves and their pet
2. user can enter their task, time duration, and priority and see it displayed
3. user can edit task with the time duration to do task and priority


- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

There should be a class named Ticket. It should have attributes:
string owner
string pet name
string dogDescription?
string task_title
string taskDescription?
int time = how long it takes to do task/ time owner should take to complete
OR
int timeHours = how many hours
int timeMinutes = how many minutes it

int priority = 1,2,3 OR string priority = high, med, low

Methods:
enter owner info = enter owner info (owner + pet + petDescription?)
edit owner info = selected info can change the existing info and save
enter task = enter task (task title, taskDescription?, timeDuration, priority)
edit task = edit info in selected task and save
task organizer = organizes the task based on priority or based on time entered
completed = task is erased from list when selected as completed

UML Diagram (created by Claude)
classDiagram
    class OwnerInfo {
        +String ownerName
        +String email
        +String phone
        +int numberOfPets
        +enterInfo()
        +editInfo()
        +addPet()
        +removePet()
    }

    class PetInfo {
        +int petId
        +String petName
        +String animalType
        +String breed
        +int age
        +enterPetInfo()
        +editPetInfo()
    }

    class Task {
        +int taskId
        +String taskName
        +String description
        +int duration
        +String priority
        +Date dateAdded
        +createTask()
        +editTask()
        +deleteTask()
    }

    class TaskList {
        +List~Task~ tasks
        +addTask()
        +removeTask()
        +sortByPriority()
        +sortByDateAdded()
        +displayList()
    }

    OwnerInfo "1" --> "0..*" PetInfo : owns
    OwnerInfo "1" --> "1" TaskList : has
    TaskList "1" --> "0..*" Task : contains
    Task "0..1" --> "0..1" PetInfo : assigned to




UML Diagram (created by CoPilot) - used
**CoPilot asked for more clarification
OwnerInfo:
    - name
    - numberOfPets
    -     classDiagram
        class OwnerInfo {
            -int ownerID
            -string name
            -string email
            -string phone
            -int numberOfPets
            +addOwnerInfo()
            +editOwnerInfo()
        }
        
        class PetInfo {
            -int petID
            -string petName
            -string animalType
            -string breed [optional]
            -int age [optional]
            +addPet()
            +editPet()
        }
        
        class Task {
            -int taskID
            -string taskName
            -int duration
            -int priority
            -datetime createdAt
            -PetInfo assignedPet [optional]
            +createTask()
            +editTask()
            +deleteTask()
        }
        
        class List {
            -int listID
            -string listName
            -string sortBy
            +addTask()
            +removeTask()
            +getTasks()
            +updateSortOrder()
        }
        
        OwnerInfo "1" --> "many" PetInfo : owns
        OwnerInfo "1" --> "many" Task : creates
        OwnerInfo "1" --> "many" List : manages
        Task "many" --> "many" PetInfo : assigns to
        List "1" --> "many" Task : contains



**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
