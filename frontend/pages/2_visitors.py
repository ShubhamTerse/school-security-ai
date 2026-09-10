import streamlit as st
import requests
import pandas as pd

API_URL = "http://localhost:8000/api"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the main page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Visitor Management")

with st.form("add_visitor_form"):
    st.subheader("Add Visitor")
    name = st.text_input("Name")
    phone = st.text_input("Phone")
    purpose = st.text_input("Purpose")
    person = st.text_input("Person to Visit")
    submitted = st.form_submit_button("Check In")
    
    if submitted:
        payload = {
            "name": name,
            "phone": phone,
            "purpose": purpose,
            "person_to_visit": person
        }
        res = requests.post(f"{API_URL}/visitors/", json=payload, headers=headers)
        if res.status_code == 200:
            st.success("Visitor Checked In Successfully!")
        else:
            st.error("Error checking in visitor.")

st.subheader("Current Visitors")
res = requests.get(f"{API_URL}/visitors/", headers=headers)
if res.status_code == 200:
    visitors = res.json()
    if visitors:
        for v in visitors:
            with st.expander(f"{v['name']} - {v['status']}"):
                st.write(f"**Phone:** {v['phone']}")
                st.write(f"**Purpose:** {v['purpose']}")
                st.write(f"**Visiting:** {v['person_to_visit']}")
                st.write(f"**Entry:** {v['entry_time']}")
                if v['status'] == 'Inside':
                    if st.button("Check Out", key=f"checkout_{v['_id']}"):
                        co_res = requests.put(f"{API_URL}/visitors/{v['_id']}/checkout", headers=headers)
                        if co_res.status_code == 200:
                            st.success("Checked out successfully!")
                            st.rerun()
    else:
        st.write("No visitors found.")
