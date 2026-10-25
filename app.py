import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")

# The Owner lives in session_state so it survives Streamlit's rerun-on-every-click
# behavior instead of being recreated (and emptied) each time.
if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_name)

owner = st.session_state.owner

st.markdown("### Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])
breed = st.text_input("Breed", value="")

if st.button("Add pet"):
    owner.add_pet(Pet(pet_name, species, breed))
    st.rerun()

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": p.name, "species": p.species, "breed": p.breed} for p in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.markdown("### Add a Task")
st.caption("Tasks are attached to the selected pet and feed directly into the scheduler.")

if owner.pets:
    pet_names = [p.name for p in owner.pets]
    selected_pet_name = st.selectbox("Pet", pet_names)
    selected_pet = next(p for p in owner.pets if p.name == selected_pet_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    task_time = st.time_input("Scheduled time")

    if st.button("Add task"):
        scheduled_minutes = task_time.hour * 60 + task_time.minute
        selected_pet.add_task(
            Task(task_title, scheduled_minutes, int(duration), priority, "daily")
        )
        st.rerun()
else:
    st.info("Add a pet first before adding tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "pet": t.pet.name,
                "task": t.description,
                "duration_minutes": t.duration_minutes,
                "priority": t.priority,
            }
            for t in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates today's plan across every pet this owner has.")

available_minutes = st.number_input(
    "Available minutes today", min_value=1, max_value=1440, value=90
)

if st.button("Generate schedule"):
    scheduler = Scheduler()
    plan = scheduler.generate_plan(owner, int(available_minutes))
    st.markdown("#### Today's Schedule")
    st.text(scheduler.explain_plan(plan))
