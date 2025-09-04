import streamlit as st
import sqlite3
from datetime import datetime

# ----------------- DB Setup -----------------
def init_db():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_task(task):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("INSERT INTO tasks (task, status, timestamp) VALUES (?, ?, ?)",
              (task, "Pending", datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_tasks():
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("SELECT * FROM tasks")
    rows = c.fetchall()
    conn.close()
    return rows

def update_status(task_id, status):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("UPDATE tasks SET status=? WHERE id=?", (status, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect("tasks.db")
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()
    conn.close()

# ----------------- Streamlit UI -----------------
st.set_page_config(page_title="To-Do List", page_icon="✅", layout="centered")

st.markdown("<h1 style='text-align:center;'>📝 To-Do List (with SQLite)</h1>", unsafe_allow_html=True)

# Initialize DB
init_db()

# Input for new task
st.subheader("➕ Add a New Task")
new_task = st.text_input("Enter your task:")
if st.button("Add Task", use_container_width=True):
    if new_task.strip():
        add_task(new_task.strip())
        st.success(f"✅ Task added: {new_task}")
        st.rerun()
    else:
        st.warning("⚠️ Please enter a task before adding.")

st.markdown("---")

# Show tasks
st.subheader("📌 Your Tasks")
tasks = get_tasks()
if tasks:
    for task_id, task, status, timestamp in tasks:
        col1, col2, col3, col4 = st.columns([5, 2, 1, 1])
        with col1:
            if status == "Done":
                st.markdown(f"<span style='color:green;'>✔️ {task}</span>", unsafe_allow_html=True)
            else:
                st.write(task)
            st.caption(f"🕒 Added: {timestamp}")
        with col2:
            if status == "Pending":
                if st.button("✅ Done", key=f"done{task_id}"):
                    update_status(task_id, "Done")
                    st.rerun()
        with col3:
            if status == "Done":
                if st.button("↩️ Undo", key=f"undo{task_id}"):
                    update_status(task_id, "Pending")
                    st.rerun()
        with col4:
            if st.button("🗑️", key=f"del{task_id}", help="Delete Task"):
                delete_task(task_id)
                st.rerun()
else:
    st.info("🎉 No tasks yet! Add some above.")
