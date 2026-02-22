# ===============================
# AI Personalized Workout & Diet Planner
# Internship-Grade UI (Refactored)
# ===============================

import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import json
from fpdf import FPDF
import io
import matplotlib.pyplot as plt

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(
    page_title="AI Workout & Diet Planner",
    page_icon="🏋️",
    layout="wide"
)

# -------------------------------
# HELPER FUNCTIONS
# -------------------------------
def estimate_calories(age, weight, height, gender, goal):
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    maintenance = bmr * 1.4

    if goal == "Lose fat":
        return int(maintenance * 0.8)
    elif goal == "Build muscle":
        return int(maintenance * 1.15)
    else:
        return int(maintenance)


def generate_sample_plan(days_count):
    days = []
    for i in range(days_count):
        days.append({
            "day": i + 1,
            "date": (datetime.now() + timedelta(days=i)).strftime("%d %b %Y"),
            "workout": [
                {"time": "7:00 AM", "exercise": "Push-ups", "details": "3 x 12"},
                {"time": "7:30 AM", "exercise": "Jogging", "details": "20 min"}
            ],
            "diet": [
                {"meal": "Breakfast", "menu": "Oats with fruits", "calories": 350},
                {"meal": "Lunch", "menu": "Grilled chicken salad", "calories": 500},
                {"meal": "Dinner", "menu": "Veg stir fry & rice", "calories": 450}
            ],
            "tips": "Drink water and sleep 7+ hours"
        })
    return days


def create_pdf(plan):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Workout & Diet Plan", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Arial", "", 12)
    for day in plan:
        pdf.cell(0, 8, f"Day {day['day']} - {day['date']}", ln=True)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, "Workout:", ln=True)
        pdf.set_font("Arial", "", 11)

        for w in day["workout"]:
            pdf.multi_cell(0, 6, f"- {w['time']} | {w['exercise']} ({w['details']})")

        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 6, "Diet:", ln=True)
        pdf.set_font("Arial", "", 11)

        for m in day["diet"]:
            pdf.multi_cell(0, 6, f"- {m['meal']}: {m['menu']} ({m['calories']} kcal)")

        pdf.ln(3)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer


# -------------------------------
# SIDEBAR – INPUT PANEL
# -------------------------------
st.sidebar.title("⚙️ Profile Settings")

age = st.sidebar.number_input("Age", 15, 60, 22)
weight = st.sidebar.number_input("Weight (kg)", 40, 150, 65)
height = st.sidebar.number_input("Height (cm)", 140, 210, 170)

gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
goal = st.sidebar.selectbox(
    "Fitness Goal",
    ["Build muscle", "Lose fat", "Maintain fitness"]
)

plan_days = st.sidebar.slider("Plan Duration (days)", 1, 14, 3)

generate = st.sidebar.button("🚀 Generate Plan")

# -------------------------------
# MAIN HEADER
# -------------------------------
st.title("🏋️ AI Personalized Workout & Diet Planner")
st.caption("Internship-ready fitness planning app using Streamlit & AI logic")

daily_cal = estimate_calories(age, weight, height, gender, goal)

# -------------------------------
# METRICS
# -------------------------------
m1, m2, m3 = st.columns(3)
m1.metric("🔥 Daily Calories", f"{daily_cal} kcal")
m2.metric("📅 Plan Duration", f"{plan_days} days")
m3.metric("🎯 Goal", goal)

# -------------------------------
# PLAN GENERATION
# -------------------------------
if "plan" not in st.session_state:
    st.session_state.plan = None

if generate:
    with st.spinner("Generating your personalized plan..."):
        st.session_state.plan = generate_sample_plan(plan_days)
    st.success("Plan generated successfully!")

plan = st.session_state.plan

# -------------------------------
# DISPLAY PLAN
# -------------------------------
if plan:
    st.divider()
    st.header("📋 Your Workout & Diet Plan")

    for day in plan:
        with st.expander(f"Day {day['day']} • {day['date']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("🏋️ Workout")
                for w in day["workout"]:
                    st.write(f"• {w['time']} – {w['exercise']} ({w['details']})")

            with col2:
                st.subheader("🥗 Diet")
                for m in day["diet"]:
                    st.write(f"• {m['meal']}: {m['menu']} ({m['calories']} kcal)")

            st.info(f"💡 Tip: {day['tips']}")

# -------------------------------
# EXPORT SECTION
# -------------------------------
st.divider()
st.header("📤 Export Plan")

if plan:
    export_type = st.selectbox("Choose format", ["JSON", "CSV", "PDF"])

    if export_type == "JSON":
        st.download_button(
            "Download JSON",
            json.dumps(plan, indent=2),
            file_name="workout_plan.json"
        )

    elif export_type == "CSV":
        rows = []
        for d in plan:
            for m in d["diet"]:
                rows.append({
                    "Day": d["day"],
                    "Date": d["date"],
                    "Meal": m["meal"],
                    "Menu": m["menu"],
                    "Calories": m["calories"]
                })
        df = pd.DataFrame(rows)
        st.download_button(
            "Download CSV",
            df.to_csv(index=False),
            file_name="workout_plan.csv"
        )

    elif export_type == "PDF":
        pdf = create_pdf(plan)
        st.download_button(
            "Download PDF",
            pdf,
            file_name="workout_plan.pdf",
            mime="application/pdf"
        )
else:
    st.warning("Generate a plan to enable downloads.")

st.success("✅ Internship-grade app ready for deployment!")