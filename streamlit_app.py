import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Employee Management", layout="wide")
st.title("Employee Management System")

menu = ["View All", "Create", "Update", "Delete", "View One"]
choice = st.sidebar.selectbox("Menu", menu)

def api_get(url):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def api_post(url, data):
    try:
        resp = requests.post(url, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def api_put(url, data):
    try:
        resp = requests.put(url, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def api_delete(url):
    try:
        resp = requests.delete(url)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        st.error(f"Error: {e}")
        return None

if choice == "View All":
    st.subheader("All Employees")
    if st.button("Refresh"):
        pass
    data = api_get(f"{API_BASE}/emp")
    if data:
        st.dataframe(data, use_container_width=True)

elif choice == "Create":
    st.subheader("Create Employee")
    with st.form("create_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=25)
        submitted = st.form_submit_button("Create")
        if submitted and name:
            result = api_post(f"{API_BASE}/emp", {"name": name, "age": age})
            if result:
                st.success(f"Employee created with ID: {result.get('id')}")

elif choice == "View One":
    st.subheader("View Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1)
    if st.button("Fetch"):
        data = api_get(f"{API_BASE}/emp/{emp_id}")
        if data:
            if "message" in data:
                st.error(data["message"])
            else:
                st.json(data)

elif choice == "Update":
    st.subheader("Update Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1, key="update_id")
    with st.form("update_form"):
        name = st.text_input("Name", key="update_name")
        age = st.number_input("Age", min_value=1, max_value=100, value=25, key="update_age")
        submitted = st.form_submit_button("Update")
        if submitted and name:
            result = api_put(f"{API_BASE}/emp/{emp_id}", {"name": name, "age": age})
            if result:
                st.success(result.get("message", "Updated"))

elif choice == "Delete":
    st.subheader("Delete Employee")
    emp_id = st.number_input("Employee ID", min_value=1, step=1, key="delete_id")
    if st.button("Delete", type="primary"):
        result = api_delete(f"{API_BASE}/emp/{emp_id}")
        if result:
            st.success(result.get("message", "Deleted"))