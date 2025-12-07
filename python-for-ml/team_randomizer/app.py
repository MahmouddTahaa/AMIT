import streamlit as st
import sqlite3
import random
import os

conn = sqlite3.connect('./student_db.db', check_same_thread=False)
cursor = conn.cursor()

def reset_database():
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM teams")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='teams'")
    for _ in range(3):
        cursor.execute("INSERT INTO teams (available_slots) VALUES (4)")
    conn.commit()
    st.success("Database has been reset! 3 fresh teams with 4 slots each.")

st.set_page_config(page_title="Students Page", layout="centered")
st.markdown("<h1 style='text-align: center; color: #FF4B4B;'>Student Random Team Assignment🤝👥</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Enter your details below</p>", unsafe_allow_html=True)

with st.expander("Admin Tools - Reset Database -PLEASE DON'T TOUCH-", expanded=False):
    st.warning("This will delete all students and reset teams!")
    if st.button("Yes, Reset Everything", type="primary"):
        reset_database()
        st.rerun()

with st.form("student_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        first_name = st.text_input("First Name", placeholder="Tamer").strip()
    with col2:
        last_name = st.text_input("Last Name", placeholder="El Gayar").strip()
    submit = st.form_submit_button("Submit")

if submit:
    if first_name and last_name:
        cursor.execute("SELECT id FROM teams")
        teams = [row[0] for row in cursor.fetchall()]
        available_teams = []
        for team_id in teams:
            cursor.execute("SELECT COUNT(*) FROM students WHERE assigned_team = ?", (team_id,))
            count = cursor.fetchone()[0]
            if count < 4:
                available_teams.append(team_id)
        if not available_teams:
            st.warning("All teams are full!")
        else:
            assigned_team = random.choice(available_teams)
            cursor.execute(
                "INSERT INTO students (first_name, last_name, assigned_team) VALUES (?, ?, ?)",
                (first_name, last_name, assigned_team)
            )
            conn.commit()
            st.balloons()
            st.success(f"Congratulations! You have been assigned to a team. Team number: {assigned_team}")
            cursor.execute("select * from students")
            rows = cursor.fetchall()
            st.write(rows)
    else:
        st.error("Please enter both first name and last name.")



conn.close()