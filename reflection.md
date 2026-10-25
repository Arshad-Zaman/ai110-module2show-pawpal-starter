# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I chose the following classes:
1. Owner: An owner owns one or many pets and he can add or remove pets.
2. Pet: A pet has one to many tasks associated with it.
3. Task: Contains detailed information about a task.
4. Scheduler: Responsible for generating a plan for the user.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Initially, there was no concrete decision on how to represent when a task happens, only how long it takes. Since a pet gets walked or fed multiple times a day, I added a scheduled_time field to Task so each occurrence is its own object and conflicts between tasks can actually be checked.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Scheduler.detect_conflicts() checks every task against every other task (a simple pairwise loop), instead of sorting tasks by time first and only comparing neighbors. That's O(n²) instead of O(n log n). I went with pairwise because it's reasonable for this scenario: a single owner's tasks for one day is at most a few dozen items, so the extra comparisons cost nothing in practice, and the pairwise version is a lot easier to read and verify than a sweep-line approach. If PawPal+ ever scheduled across a whole household for a week or month instead of a day, this would be worth revisiting.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI mainly for design brainstorming and review. I had it draft the first UML diagram, then asked it to review the diagram for unnecessary complexity and bad relationships before I touched any code. The most helpful prompts were ones that asked it to review something I already had instead of generating from scratch, like "review the diagram" or "any missing relationships or bottlenecks."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI originally gave Scheduler two relationships to Task and Pet, and gave Owner a preferences dict. I rejected both: the extra Scheduler relationship was redundant since it only depends on Task, and preferences wasn't being used anywhere, so I had it removed. I verified the scheduling logic itself by running main.py and checking the printed schedule matched what I expected, and by writing tests in tests/test_pawpal.py to confirm mark_complete() and add_task() actually changed state.

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
