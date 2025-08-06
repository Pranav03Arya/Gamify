# app.py

import streamlit as st
import pandas as pd
import random

# ---------------------
# Theme Toggle
# ---------------------
theme = st.sidebar.radio("Select Theme", ["Light", "Dark"])

if theme == "Dark":
    st.markdown(
        """
        <style>
            body { background-color: #1e1e1e; color: #f1f1f1; }
            .stButton>button { background-color: #333; color: #f1f1f1; }
            .stSlider>div>div>div>div { background-color: #444; }
            .stMarkdown, .stDataFrame { color: #f1f1f1; }
            .stMetric [data-testid="stMetricValue"] { color: #f1f1f1; }
        </style>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        """
        <style>
            body { background-color: #FFFFFF; color: #000000; }
        </style>
        """,
        unsafe_allow_html=True
    )

# ---------------------
# Game Constants & Events
# ---------------------
YEARS = 10
CAPITAL_NEEDED = 100_000
BASE_INTEREST_RATE = 0.08

EVENTS = [
    {"name": "Interest Rate Hike", "effect": 0.02, "message": "📈 The central bank raised interest rates!"},
    {"name": "Market Boom",       "effect": -20000, "message": "🚀 Market boom! Valuation jumps!"},
    {"name": "Recession Warning", "effect": 15000,  "message": "📉 Recession fears hurt your valuation."},
    {"name": "Stable Year",       "effect": 0,      "message": "😌 A stable year with no surprises."},
]

# ---------------------
# Session State Initialization
# ---------------------
if 'year' not in st.session_state:
    st.session_state.year = 1
    st.session_state.history = []
    st.session_state.valuation = 1_000_000
    st.session_state.ownership = 100

# ---------------------
# App Title
# ---------------------
st.title("💼 CFO's Dilemma: Capital Structure Simulator")
st.subheader(f"Year {st.session_state.year} of {YEARS}")

# ---------------------
# User Input
# ---------------------
debt_percent = st.slider("Choose % Debt", 0, 100, 50)
equity_percent = 100 - debt_percent

# ---------------------
# Random Event for This Year
# ---------------------
event = random.choice(EVENTS)
st.info(event["message"])

# ---------------------
# Financial Calculations
# ---------------------
debt_amount = CAPITAL_NEEDED * (debt_percent / 100)
equity_amount = CAPITAL_NEEDED * (equity_percent / 100)

# Adjust interest rate if event is rate hike
interest_rate = BASE_INTEREST_RATE + (event["effect"] if event["name"] == "Interest Rate Hike" else 0)
interest_payment = round(debt_amount * interest_rate, 2)

# only dilute when you actually issue equity  
if equity_percent > 0:  
    ownership_left = st.session_state.ownership * (equity_percent / 100)  
else:  
    ownership_left = st.session_state.ownership  

risk_score = min(100, round((debt_amount / (equity_amount + 1)) * 10))

# Valuation change includes event.effect for non-rate events as a direct bump/penalty
valuation_change = -interest_payment - (risk_score * 100) + 5_000 - (event["effect"] if event["name"] != "Interest Rate Hike" else 0)
new_valuation = st.session_state.valuation + valuation_change

# ---------------------
# Submit Decision
# ---------------------
if st.button("Submit Decision"):
    st.session_state.history.append({
        "Year": st.session_state.year,
        "Debt %": debt_percent,
        "Equity %": equity_percent,
        "Interest Rate": f"{round(interest_rate*100, 2)}%",
        "Interest Paid": interest_payment,
        "Ownership %": round(ownership_left, 2),
        "Risk Score": risk_score,
        "Valuation": round(new_valuation, 2),
        "Event": event["name"]
    })
    st.session_state.year += 1
    st.session_state.valuation = new_valuation
    st.session_state.ownership = ownership_left

# ---------------------
# Show Simulation History & Chart
# ---------------------
if st.session_state.history:
    st.subheader("📊 Simulation Results")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index("Year")["Valuation"])

# ---------------------
# End of Game Summary
# ---------------------
if st.session_state.year > YEARS:
    st.success("🎉 Game Over! You've completed all simulation rounds.")
    st.metric("🏁 Final Company Valuation", f"${round(st.session_state.valuation, 2)}")
    st.metric("🔐 Final Ownership", f"{round(st.session_state.ownership, 2)}%")
    # CSV Download
    csv = pd.DataFrame(st.session_state.history).to_csv(index=False)
    st.download_button("📥 Download Report", data=csv, file_name="simulation_results.csv", mime="text/csv")
    # Restart
    if st.button("🔁 Restart"):
        for key in ("year", "history", "valuation", "ownership"):
            del st.session_state[key]
