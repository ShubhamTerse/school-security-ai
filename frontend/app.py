import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="School Security AI", layout="wide", initial_sidebar_state="expanded")

API_URL = "http://localhost:8000/api"

if "token" not in st.session_state:
    st.session_state.token = None
if "username" not in st.session_state:
    st.session_state.username = None

def login(username, password):
    response = requests.post(f"{API_URL}/auth/login", data={"username": username, "password": password})
    if response.status_code == 200:
        data = response.json()
        st.session_state.token = data["access_token"]
        st.session_state.username = username
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error("Invalid credentials")

def logout():
    st.session_state.token = None
    st.session_state.username = None
    st.rerun()

st.title("School Security Administration System")

if not st.session_state.token:
    st.subheader("Login")
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            login(username, password)
            
    st.subheader("Register (Demo purposes)")
    with st.form("register_form"):
        reg_user = st.text_input("New Username")
        reg_pass = st.text_input("New Password", type="password")
        reg_role = st.selectbox("Role", ["Admin", "Security Officer", "Teacher"])
        reg_submit = st.form_submit_button("Register")
        if reg_submit:
            res = requests.post(f"{API_URL}/auth/register", json={"username": reg_user, "password": reg_pass, "role": reg_role})
            if res.status_code == 200:
                st.success("Registered successfully! You can now login.")
            else:
                st.error(f"Registration failed: {res.text}")
else:
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    if st.sidebar.button("Logout"):
        logout()
        
    st.write("Please use the sidebar to navigate to Dashboard, Visitors, Incidents, or Chatbot.")
