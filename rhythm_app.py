
#BASIC DESIGN OF RHYTHM HOW IT WILL GOING TO WORK !!!


import streamlit as st
from datetime import datetime, timedelta
st.markdown(f"👋 Welcome back! Let’s get your rhythm flowing today.")

st.set_page_config(page_title="Rhythm - Your Daily Planner", layout="centered")

st.title("🎧 Rhythm – Your Smart Daily Planner")
st.markdown("Enter your daily routine and emotion to generate your personalized schedule.")





# 1. INPUTS (keep outside the button)

wake_time = st.time_input("⏰ Wake-up Time", value=datetime.strptime("06:00", "%H:%M").time(), key="wake_time")
sleep_time = st.time_input("🌙 Sleep Time", value=datetime.strptime("22:00", "%H:%M").time(), key="sleep_time")

study_hours = st.slider("📖 Study Hours", 0, 12, 5 , key = "study_hours")
play_hours = st.slider("🎮 Play Hours", 0, 6, 2 , key="play_hours")

emotion = st.selectbox("🧠 How do you feel today?", ["Happy", "Motivated", "Sad", "Tired"] , key="emotion")
goal = st.selectbox("🎯 Your Goal", ["Exam Prep", "Skill Learning", "Health", "Consistency"], key="goal")

st.markdown("### 💬 Want to share how you're feeling today?")
user_problem = st.text_input("Tell Rhythm what’s on your mind:",key="user_problem")


# 2. GENERATE ONLY ON BUTTON

if st.button("✅ Generate My Daily Plan"):

    wake = datetime.combine(datetime.today(), wake_time)
    sleep = datetime.combine(datetime.today(), sleep_time)
    total_hours = int((sleep - wake).seconds // 3600)

    current_time = wake
    plan = []

    # Motivation message
    messages = {
        "Sad": "💛 You said you're feeling low today. That’s okay. Let’s take one steady step at a time.",
        "Happy": "🌟 You’re glowing today! Let’s lock in that focus and do something amazing.",
        "Tired": "😴 Energy is low, but you showed up. That’s everything. Let’s go gently.",
        "Motivated": "🔥 You’re on fire today. We’ll match your energy with a focused plan."
    }

    st.markdown(f"### 💬 Motivation: {messages.get(emotion)}")

    # Problem-based quote
    problem = user_problem.lower()
    if "lazy" in problem or "unmotivated" in problem:
        st.info("💡 Discipline > Motivation. Just start with one small task.")
        st.success("Quote: 'You don’t have to be extreme. Just consistent.'")
    elif "missed" in problem or "yesterday" in problem:
        st.info("🕊️ One off day doesn’t define you. Showing up today matters most.")
        st.success("Quote: 'Start again. You’re still in the game.'")
    elif "pressure" in problem or "overwhelmed" in problem:
        st.info("🌿 Pressure fades with clarity. Let’s break the day into small wins.")
        st.success("Quote: 'Progress is peace. Not perfection.'")
    elif "tired" in problem or "exhausted" in problem:
        st.info("😴 Rest isn’t failure. You’ve come far. We’ll go easy today.")
        st.success("Quote: 'Even a step forward while tired is strength.'")
    elif problem != "":
        st.info("🧠 Thanks for sharing. Rhythm is with you today.")
        st.success("Quote: 'Show up. Adjust. Win anyway.'")

    # New scheduler logic (with balance)
    remaining_study = study_hours
    remaining_play = play_hours
    remaining_break = 2
    study_chunk = 0

    def add_hour_block(activity):
        global current_time
        end_time = current_time + timedelta(hours=1)
        plan.append({
            "Time": f"{current_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}",
            "Activity": activity
        })
        current_time = end_time

    while current_time + timedelta(hours=1) <= sleep:
        if remaining_study > 0:
            add_hour_block("Study")
            remaining_study -= 1
            study_chunk += 1

            if study_chunk == 2 and remaining_break > 0:
                add_hour_block("Break")
                remaining_break -= 1
                study_chunk = 0

            elif study_chunk == 2 and remaining_play > 0:
                add_hour_block("Play")
                remaining_play -= 1
                study_chunk = 0

        elif remaining_play > 0:
            add_hour_block("Play")
            remaining_play -= 1

        elif remaining_break > 0:
            add_hour_block("Break")
            remaining_break -= 1

        else:
            add_hour_block("Free/Flex")

    # Show table
    st.markdown("### 🗓️ Your Daily Plan")
    st.table(plan)
