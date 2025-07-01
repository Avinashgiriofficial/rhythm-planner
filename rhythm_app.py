#---------BETA VERSION OF RHYTHM-------------

import streamlit as st
from datetime import datetime, date, timedelta
from streamlit_calendar import calendar
import pandas as pd
import os

# -------------- PAGE CONFIG (must be first) -----------------
st.set_page_config(page_title="Rhythm – Your Daily Planner", layout="centered")
st.info("⏳ Waking up... Please wait a few seconds while the app loads.")

# ----------------- CALENDAR WIDGET --------------------------
st.markdown("### 📅 Your Monthly Calendar")
calendar(
    events=[{
        "title": "Today",
        "start": date.today().isoformat(),
        "end": date.today().isoformat(),
        "color": "#ff6f61"
    }],
    options={"initialView": "dayGridMonth"},
    custom_css="""
        .fc .fc-daygrid-day.fc-day-today {
            background-color: #ffe2dc;
            border: 2px solid #ff6f61;
        }
    """
)

# ----------------- HEADER / INPUTS --------------------------

today_tab, week_tab, feedback_tab = st.tabs(["📅 Today", "📈 Weekly Stats", "📣 Feedback"])

# ------------------ TODAY TAB ------------------
with today_tab:
    st.markdown("👋 Welcome back! Let’s get your rhythm flowing today.")
    st.title("🎧 Rhythm – Your Smart Daily Planner")
    st.markdown("Enter your daily routine and emotion to generate your personalized schedule.")

    # Your input widgets go here 👇
    wake_time = st.time_input("⏰ Wake‑up Time", value=datetime.strptime("06:00", "%H:%M").time())
    sleep_time = st.time_input("🌙 Sleep Time", value=datetime.strptime("22:00", "%H:%M").time())
    study_hours = st.slider("📖 Study Hours", 0, 12, 5)
    play_hours = st.slider("🎮 Play Hours", 0, 6, 2)

    emotion = st.selectbox("🧠 How do you feel today?", ["Happy", "Motivated", "Sad", "Tired"])
    goal = st.selectbox("🎯 Your Goal", ["Exam Prep", "Skill Learning", "Health", "Consistency"])

    st.markdown("### 💬 Want to share how you're feeling today?")
    user_problem = st.text_input("Tell Rhythm what’s on your mind:")


from textblob import TextBlob

def generate_response(text, mood):
    text = text.lower()
    sentiment = TextBlob(text).sentiment.polarity

    if not text.strip():
        return None

    # Mood-based empathy
    if sentiment < -0.3:
        return "💛 It's okay to feel low. Let's take small, kind steps today."

    # Keyword-based tips
    elif "lazy" in text or "unmotivated" in text:
        return "💡 Start with just 5 minutes. Action brings motivation, not the other way around."

    elif "missed" in text or "yesterday" in text:
        return "🔁 Yesterday is over. Restart strong today. You're not behind — you're learning."

    elif "tired" in text or "exhausted" in text:
        return "😴 A short nap, water, and a reset can do wonders. Energy matters more than hours."

    elif "pressure" in text or "overwhelmed" in text:
        return "🌿 Break the big goal into tiny wins. One thing at a time."

    elif "phone" in text or "distraction" in text:
        return "📵 Try putting your phone away for just 30 minutes. You'll feel clarity quickly."

    elif "anxious" in text or "fear" in text:
        return "🧘 Deep breaths. Remember — your effort is enough. You're not alone."

    elif "confused" in text or "don't know what to study" in text:
        return "🎯 Pick the smallest topic. Start there. Clarity comes after action."

    # Emotion-specific override
    elif mood == "Tired":
        return "Take it slow today. Even a little progress counts."

    elif mood == "Motivated":
        return "You're on fire today 🔥 Let’s use that momentum with full focus!"

    elif sentiment > 0.5:
        return "You're sounding positive! Let's lock that in and make today productive. 💪"

    return "✨ Thanks for sharing. You’re doing better than you think. Let’s go one task at a time."


# ------------------ MAIN ACTION BUTTON ----------------------

if st.button("✅ Generate My Daily Plan"):
    # Smart reply after user shares a problem
    if user_problem:
        coach_reply = generate_response(user_problem, emotion)
    if coach_reply:
        st.markdown("### 💬 Rhythm’s Response")
        st.success(coach_reply)

    # --- Convert times into full datetimes ---
    today    = datetime.today()
    wake_dt  = datetime.combine(today, wake_time)
    sleep_dt = datetime.combine(today, sleep_time)
    if sleep_dt <= wake_dt:            # handle overnight schedules
        sleep_dt += timedelta(days=1)
# 👇 Add this before log_entry
    reflection_mood = st.radio("How did your day feel overall?", ["😊 Great", "😐 Okay", "😞 Tough"], key="reflection_mood")
    reflection_note = st.text_area("Any thoughts you'd like to share?", placeholder="Felt productive / Got distracted / etc.", key="reflection_note")


 # ---------------- SAVE DAILY LOG ------------------------
    
    
    log_entry = {
        "Date": today.strftime("%Y-%m-%d"),
        "Wake": wake_time.strftime("%H:%M"),
        "Sleep": sleep_time.strftime("%H:%M"),
        "Study Hours": study_hours,
        "Play Hours": play_hours,
        "Emotion": emotion,
        "Goal": goal,
        "Problem": user_problem,
        "Motivational Quote": "You don’t have to be extreme. Just consistent.",
        "Reflection Mood": reflection_mood,
        "Reflection Note": reflection_note
        
        }

    file_path = "rhythm_user_log.csv"
    df_entry  = pd.DataFrame([log_entry])
    df_entry.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
    st.success("✅ Your data has been saved!")
    

    # ---------------- MOTIVATION BLOCK ----------------------
    
    messages = {
        "Sad":       "💛 You said you're feeling low today. That’s okay. Let’s take one steady step at a time.",
        "Happy":     "🌟 You’re glowing today! Let’s lock in that focus and do something amazing.",
        "Tired":     "😴 Energy is low, but you showed up. That’s everything. Let’s go gently.",
        "Motivated": "🔥 You’re on fire today. We’ll match your energy with a focused plan."
    }
    st.markdown(f"### 💬 Motivation: {messages.get(emotion)}")

    
    # (keep your problem‑specific quote logic here if desired)
    # --------------- BUILD THE HOURLY PLAN ------------------
    
    
    remaining_study = study_hours
    remaining_play  = play_hours
    remaining_break = 2          # two breaks to sprinkle in
    study_chunk     = 0
    current_time    = wake_dt
    plan            = []

    def add_hour_block(current_time, activity):
         end_time = current_time + timedelta(hours=1)
         plan.append({
        "Time": f"{current_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}",
        "Activity": activity
    })
         return end_time
    

# ----------------Combine times to datetime--------------------------

today = datetime.today()    
wake_dt = datetime.combine(today, wake_time)
sleep_dt = datetime.combine(today, sleep_time)
if sleep_dt <= wake_dt:
    sleep_dt += timedelta(days=1)

current_time = wake_dt  # ✅ This is required before using it below
plan = []

def add_hour_block(current_time, activity):
    end_time = current_time + timedelta(hours=1)
    plan.append({
        "Time": f"{current_time.strftime('%I:%M %p')} – {end_time.strftime('%I:%M %p')}",
        "Activity": activity
    })
    return end_time


remaining_study = study_hours
remaining_play = play_hours
remaining_break = 2
study_chunk = 0

#------------------------SCHEDULING LOOP---------------------------

from random import shuffle

# Create all hourly blocks
time_blocks = []
t = wake_dt
while t + timedelta(hours=1) <= sleep_dt:
    time_blocks.append(t.strftime("%I:%M %p") + " - " + (t + timedelta(hours=1)).strftime("%I:%M %p"))
    t += timedelta(hours=1)

# Create the schedule plan
activities = (["Study"] * remaining_study +
              ["Play"] * remaining_play +
              ["Break"] * remaining_break)

# Fill rest with Flex
activities += ["Free/Flex"] * (len(time_blocks) - len(activities))

# Shuffle to avoid stacking Study only at morning
shuffle(activities)

# Now create the plan
plan = []
for i in range(len(time_blocks)):
    plan.append({
        "Time": time_blocks[i],
        "Activity": activities[i]
    })
# ------------------ FEEDBACK TAB ------------------
with feedback_tab:
    st.header("📣 We'd love your feedback!")
    st.markdown("**Share your thoughts — it only takes 30 seconds.**")

    # Option 1: Clickable form link
    st.markdown("[📝 Open Feedback Form](https://forms.gle/5GagUQeUxbv8odUW9)")



    # ------------------ SHOW THE PLAN ----------------------
st.markdown("### 🗓️ Your Daily Plan")
st.table(pd.DataFrame(plan))
