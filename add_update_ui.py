import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"


def add_update_tab():
    # keep a stable key for the date input so session_state can detect changes
    selected_date = st.date_input("Enter Date", datetime(2025, 10, 1), key="selected_date", label_visibility="collapsed")

    # initialize session_state containers
    if "expenses" not in st.session_state:
        st.session_state.expenses = []
    if "last_loaded_date" not in st.session_state:
        st.session_state.last_loaded_date = None

    # When the selected date changes (or first load), fetch from backend
    # Use ISO format to be safe for the API endpoint
    selected_date_str = selected_date.strftime("%Y-%m-%d")
    if st.session_state.last_loaded_date != selected_date_str:
        try:
            resp = requests.get(f"{API_URL}/expenses/{selected_date_str}")
            if resp.status_code == 200:
                st.session_state.expenses = resp.json()
            else:
                st.session_state.expenses = []
                st.error("Failed to retrieve expenses for selected date.")
        except Exception as e:
            st.session_state.expenses = []
            st.error(f"Error fetching expenses: {e}")
        st.session_state.last_loaded_date = selected_date_str

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Build the form using values from session_state so changes reflect immediately on rerun
    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        # Ensure we have at least 5 rows in session_state to show
        while len(st.session_state.expenses) < 5:
            st.session_state.expenses.append({"amount": 0.0, "category": "Shopping", "notes": ""})

        # Render inputs bound to session_state keys
        for i in range(5):
            # safe access
            row = st.session_state.expenses[i] if i < len(st.session_state.expenses) else {"amount": 0.0, "category": "Shopping", "notes": ""}

            col1, col2, col3 = st.columns(3)
            with col1:
                new_amount = st.number_input(
                    label=f"Amount {i}",
                    min_value=0.0,
                    step=1.0,
                    value=float(row.get("amount", 0.0)),
                    key=f"amount_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                # compute index safely (default to 0 if category not found)
                default_index = categories.index(row.get("category")) if row.get("category") in categories else 0
                new_category = st.selectbox(
                    label=f"Category {i}",
                    options=categories,
                    index=default_index,
                    key=f"category_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                new_notes = st.text_input(
                    label=f"Notes {i}",
                    value=row.get("notes", ""),
                    key=f"notes_{selected_date_str}_{i}",
                    label_visibility="collapsed"
                )

            # Update the in-memory row immediately so it persists across reruns
            st.session_state.expenses[i] = {
                "amount": new_amount,
                "category": new_category,
                "notes": new_notes
            }

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # filter out zero-amount rows before sending
            filtered_expenses = [expense for expense in st.session_state.expenses if expense.get("amount", 0) > 0]
            try:
                post_resp = requests.post(f"{API_URL}/expenses/{selected_date_str}", json=filtered_expenses)
                if post_resp.status_code == 200:
                    st.success("Expenses updated successfully!")
                    # reload from server to reflect any server-side changes
                    st.session_state.last_loaded_date = None
                else:
                    st.error("Failed to update expenses.")
            except Exception as e:
                st.error(f"Error updating expenses: {e}")
