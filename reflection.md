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

The scheduler considers three constraints: priority (high/medium/low), the owner's available time budget, and scheduled time (for conflict detection, separate from the plan). Priority and the time budget mattered most because generate_plan() trades them off directly: high-priority tasks get scheduled first, and lower-priority ones get dropped once the budget runs out. Scheduled time is a different problem entirely, it doesn't decide what's in the plan, it catches tasks that would physically collide after the fact.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

Scheduler.detect_conflicts() checks every task against every other task — O(n²) — instead of sorting by time first and only comparing neighbors (O(n log n)). That's reasonable here: a single owner's day is at most a few dozen tasks, so the extra comparisons cost nothing, and pairwise is far easier to read and verify than a sweep-line approach. Worth revisiting if PawPal+ ever scheduled a whole household for a week or month instead of a day.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI mainly for design brainstorming and review: drafting the first UML diagram, then asking it to review that diagram for unnecessary complexity or bad relationships before writing any code. The most helpful prompts asked it to critique something I already had rather than generate from scratch — "review the diagram," "any missing relationships or bottlenecks."

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

The AI originally gave Scheduler two relationships (to Task and Pet) and gave Owner a preferences dict. I rejected both: the extra Scheduler relationship was redundant since it only depends on Task, and preferences wasn't used anywhere. I verified the real scheduling logic by running main.py and checking the printed schedule matched expectations, and by writing tests in tests/test_pawpal.py to confirm mark_complete() and add_task() actually changed state.

**c. AI Strategy**

- Which AI coding assistant features were most effective for building your scheduler?
- Give one example of an AI suggestion you rejected or modified to keep your system design clean.
- How did using separate chat sessions for different phases help you stay organized?

The most effective feature was handing the assistant my actual files (pawpal_system.py, app.py, tests/test_pawpal.py) and having it work from what was really there instead of generating something generic. Asked to update diagrams/uml.mmd into a final version, it read the real class definitions and caught things I'd have missed by hand, like Task.pet being a real relationship (set by Pet.add_task()) the original diagram never drew. The other feature I leaned on was having it actually run things, not just reason about code: running pytest to confirm the suite passed, and driving the Streamlit app in a real browser to screenshot the conflict warnings and generated schedule, instead of trusting that UI changes "looked right" from the code alone.

One suggestion I modified: the draft UML update kept a category field and a plain name attribute on Task, matching the original Phase 1 sketch. I had it cross-check against the real pawpal_system.py, where category was never implemented and the field is actually called description. I dropped category entirely rather than keep it as a "nice to have" placeholder, since an unused field would have misrepresented what the system does.

Separate chat sessions per phase (design review, implementation, testing, documentation) kept each conversation focused on one kind of judgment call. A session reviewing the UML diagram stayed about relationships and responsibilities, it didn't drift into writing test cases or wordsmithing the README. That made it easy to trace, afterward, where a given decision came from, instead of untangling one long thread where design, code, and docs decisions were all mixed together.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested sorting (mixed, unscheduled, and empty inputs), recurrence (due_date advancing a day for "daily," a week for "weekly," and not at all for "none"), and conflict detection (overlaps across pets, back-to-back tasks that shouldn't count, same-time tasks on different due_dates that also shouldn't count). These are the behaviors most prone to off-by-one and boundary bugs — the "touching but not overlapping" case in conflicts_with(), or the wrong recurrence interval — and those bugs wouldn't show up just from reading the code.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I'm confident in sort_by_time(), mark_complete(), and detect_conflicts(), since those have direct edge-case coverage. Less confident in generate_plan() as a whole — no test exercises priority-sorting and the time-budget filter together, so I can't be sure they interact as expected when, say, a high-priority task doesn't fit but a lower-priority one does. With more time I'd test generate_plan() directly, plus edge cases like duplicate task names across pets, a zero or negative available_minutes budget, and filter_tasks() with a pet_name that doesn't exist.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with the recurrence and conflict-detection logic. mark_complete() turning a completed daily or weekly task straight into its next occurrence is the one piece that made PawPal+ feel like an actual scheduling assistant rather than just a sorted list — paired with detect_conflicts() catching overlaps across pets, not just within one.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

generate_plan() only optimizes for priority and the time budget — it doesn't check the plan it produces for conflicts. The Streamlit app papers over this by running detect_conflicts() separately on the generated plan, but the scheduler itself doesn't know a plan it hands back might double-book the owner. With another iteration, I'd fold conflict-awareness into generate_plan() itself, so an internally consistent plan is the only kind it can produce.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

Being the lead architect meant the AI was fast at producing plausible structure but had no idea which parts actually mattered until I checked. It kept an unused category field, gave Owner a preferences dict nothing read, and added a redundant Scheduler relationship — none of it wrong exactly, just not load-bearing. My job wasn't to generate the design or the tests, it was to keep asking "is this actually used, does running main.py or pytest prove it works," and keep only what survived. The AI is good at drafting and at catching things I overlooked when pointed at real code; it's not a substitute for deciding what the system is supposed to do.
