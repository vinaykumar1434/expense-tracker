# Expense Tracker – Personal Finance Dashboard

A clean, fast, and fully local expense management system built with pure Python.

![preview](https://raw.githubusercontent.com/vinaykumar1434/expense-tracker/main/preview.png)

## Features
- Add/edit expenses by date (no duplicates)
- Instant category-wise analytics with percentages
- Beautiful bar charts
- 100% private – runs locally

## Tech Stack
- Frontend: **Streamlit**
- Backend: **FastAPI**
- Database: **MySQL**
- Analytics: **Pandas** + **Pydantic**

## Quick Start
```bash
pip install -r requirements.txt

# Terminal 1
uvicorn backend.server:app --reload

# Terminal 2
streamlit run frontend/app.py
