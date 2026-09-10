import streamlit as st
import requests

API_URL = "http://localhost:8000/api"

if "token" not in st.session_state or not st.session_state.token:
    st.warning("Please log in from the main page.")
    st.stop()

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.title("Incident Reporting")

with st.form("add_incident"):
    st.subheader("Report an Incident")
    title = st.text_input("Incident Title")
    location = st.text_input("Location")
    description = st.text_area("Description")
    reported_by = st.session_state.get("username", "Unknown")
    
    submitted = st.form_submit_button("Report Incident")
    if submitted:
        payload = {
            "title": title,
            "location": location,
            "description": description,
            "reported_by": reported_by
        }
        res = requests.post(f"{API_URL}/incidents/", json=payload, headers=headers)
        if res.status_code == 200:
            st.success("Incident Reported Successfully!")
        else:
            st.error("Failed to report incident.")

st.subheader("Incident List")
res = requests.get(f"{API_URL}/incidents/", headers=headers)
if res.status_code == 200:
    incidents = res.json()
    for inc in incidents:
        with st.expander(f"{inc['title']} at {inc['location']} ({inc['status']})"):
            st.write(f"**Description:** {inc['description']}")
            st.write(f"**Reported By:** {inc['reported_by']} on {inc['date_time']}")
            
            if inc.get("ai_analysis"):
                analysis = inc["ai_analysis"]
                st.write("---")
                st.markdown(f"### 🤖 AI Analysis")
                st.markdown(f"**Summary:** {analysis.get('summary')}")
                st.markdown(f"**Risk Level:** `{analysis.get('risk_level')}`")
                st.markdown(f"**Reason:** {analysis.get('risk_reason')}")
                st.markdown(f"**Category:** {analysis.get('category')}")
                st.markdown(f"**Urgency:** {analysis.get('urgency')}")
                
                st.markdown("**Recommended Actions:**")
                for action in analysis.get('recommended_actions', []):
                    st.markdown(f"- {action}")
            else:
                if st.button("Analyze with AI", key=f"analyze_{inc['_id']}"):
                    with st.spinner("Analyzing with Gemini..."):
                        analyze_res = requests.post(f"{API_URL}/ai/analyze/{inc['_id']}", headers=headers)
                        if analyze_res.status_code == 200:
                            st.success("Analysis complete!")
                            st.rerun()
                        else:
                            st.error(f"Analysis failed: {analyze_res.text}")
