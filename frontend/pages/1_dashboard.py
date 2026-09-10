import streamlit as st
import requests
import pandas as pd

API_URL = "https://school-security-ai.onrender.com/api"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the main page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Dashboard")

col1, col2, col3, col4 = st.columns(4)

# Fetch stats
visitors_req = requests.get(f"{API_URL}/visitors/", headers=headers)
incidents_req = requests.get(f"{API_URL}/incidents/", headers=headers)
emergencies_req = requests.get(f"{API_URL}/emergencies/", headers=headers)

if visitors_req.status_code == 200 and incidents_req.status_code == 200:
    visitors = visitors_req.json()
    incidents = incidents_req.json()
    emergencies = emergencies_req.json() if emergencies_req.status_code == 200 else []
    
    high_risk = sum(1 for i in incidents if i.get("ai_analysis") and i["ai_analysis"].get("risk_level") in ["HIGH", "CRITICAL"])
    
    col1.metric("Total Visitors", len(visitors))
    col2.metric("Total Incidents", len(incidents))
    col3.metric("High Risk Incidents", high_risk)
    col4.metric("Active Emergencies", len(emergencies))
    
    st.subheader("Recent Security Incidents")
    if incidents:
        # Display incidents in a dataframe
        df_incidents = pd.DataFrame(incidents)
        # Extract risk level
        def get_risk(x):
            if isinstance(x, dict):
                return x.get("risk_level", "Unknown")
            return "Pending AI Analysis"
            
        df_incidents['Risk'] = df_incidents['ai_analysis'].apply(get_risk)
        st.dataframe(df_incidents[["title", "location", "Risk", "date_time", "status"]])
    else:
        st.info("No incidents reported yet.")
else:
    st.error("Failed to load dashboard data.")
