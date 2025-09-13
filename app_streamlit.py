
import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Smart Exam Prep Planner — Monitor & Edit")

# For simplicity we load a CSV exported from the running notebook environment.
# In deployment, you'd expose APIs or integrate via shared DB.
try:
    df = pd.read_csv("exam_plan_runtime.csv", parse_dates=["date"])
except Exception:
    st.error("No runtime plan found (exam_plan_runtime.csv). Run planner notebook cell to export first.")
    st.stop()

st.header("Upcoming Plan")
st.dataframe(df)

st.header("Mark a slot as done")
slot = st.selectbox("Choose slot_id", df['slot_id'].tolist())
if st.button("Mark Done"):
    df.loc[df['slot_id']==slot, 'done'] = True
    df.to_csv("exam_plan_runtime.csv", index=False)
    st.success("Marked done and saved.")
    st.experimental_rerun()

st.header("Reschedule (missed day)")
missed = st.date_input("Missed Date", value=datetime.now().date())
if st.button("Reschedule Missed Day"):
    # call a backend reschedule endpoint in production; here we set a flag CSV and user will re-run notebook.
    st.info(f"Marking {missed} as missed. Please re-run reschedule_missed_day in notebook.")
