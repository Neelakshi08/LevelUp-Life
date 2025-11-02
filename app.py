import streamlit as st
import json
import os

st.set_page_config(page_title="LevelUp Life", page_icon="🎮")

# --- Load or initialize data ---
DATA_FILE = "progress.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"xp": 0, "level": 1, "tasks": []}, f)

def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- Main UI ---
st.title("🎮 LevelUp Life")
st.write("Gamify your real life. Complete tasks → Earn XP → Level Up!")

data = load_data()

# --- Add new task ---
st.subheader("✅ Add New Task")
task = st.text_input("Enter task name:")
xp = st.number_input("XP Reward", min_value=10, max_value=500, step=10)

if st.button("Add Task"):
    data["tasks"].append({"task": task, "xp": xp, "done": False})
    save_data(data)
    st.success("Task added!")

# --- Display tasks ---
st.subheader("📋 Your Tasks")
for i, t in enumerate(data["tasks"]):
    if not t["done"]:
        if st.checkbox(f"{t['task']} (+{t['xp']} XP)", key=i):
            data["xp"] += t["xp"]
            t["done"] = True
            data["level"] = 1 + data["xp"] // 500
            save_data(data)
            st.success(f"🎉 You gained {t['xp']} XP!")

# --- Progress display ---
st.subheader("🌟 Progress")
st.write(f"**XP:** {data['xp']} | **Level:** {data['level']}")

progress = (data["xp"] % 500) / 500
st.progress(progress)
