import streamlit as st
import requests

API_URL = "https://school-security-ai.onrender.com/api"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the main page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Emergency Management")

with st.form("add_emergency"):
    st.subheader("Report Emergency")
    em_type = st.selectbox("Type", ["Fire", "Medical Emergency", "Unauthorized Access", "Fight", "Missing Student", "Suspicious Object", "Natural Disaster", "Other"])
    location = st.text_input("Location")
    description = st.text_area("Description")
    
    submitted = st.form_submit_button("🚨 Trigger Alert 🚨")
    if submitted:
        payload = {
            "emergency_type": em_type,
            "location": location,
            "description": description
        }
        res = requests.post(f"{API_URL}/emergencies/", json=payload, headers=headers)
        if res.status_code == 200:
            st.error(f"EMERGENCY REPORTED: {em_type} at {location}!")
        else:
            st.error("Failed to report emergency.")

st.subheader("Active Emergencies")
res = requests.get(f"{API_URL}/emergencies/", headers=headers)
if res.status_code == 200:
    emergencies = res.json()
    active_ems = [e for e in emergencies if e['status'] == 'ACTIVE']
    
    if active_ems:
        for em in active_ems:
            st.error(f"🚨 {em['emergency_type']} - {em['location']} ({em['date_time']})")
            st.write(f"**Details:** {em['description']}")
            if st.button("Mark Resolved", key=f"resolve_{em['_id']}"):
                r_res = requests.put(f"{API_URL}/emergencies/{em['_id']}/resolve", headers=headers)
                if r_res.status_code == 200:
                    st.success("Emergency resolved.")
                    st.rerun()
    else:
        st.success("No active emergencies.")
