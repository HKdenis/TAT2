import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account
import os
import datetime


st.title("Technical Assistance Tracker")

# Use an icon in an info box
st.info("This is an informational message with an icon: :material/info:")

# Use an icon in the sidebar
st.sidebar.subheader("Navigation :material/list:")


st.title("🧊 Technical Assistance Tracker")
st.write("""
Welcome to the Technical Assistance Tracker! 
This application is designed to help you monitor and manage technical assistance visits.
Use the sidebar to navigate through different sections of the tracker.
""")     

st.sidebar.success('Select a page above to get started.')
#st.sidebar.write("""Note: Refresh the data entry page after report submission to clear the form.""")
st.markdown("TOTAL MENTORSHIP VISITS CONDUCTED BY MONTH AT A GLANCE")
# Load credentials from secrets.toml
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

# Create creds for gspread (oauth2client) compatibility
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scopes=scope)

client = gspread.authorize(creds)



# Read data from a specific sheet using gspread
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1EXvYhyOEhK1zYG7I5e4c4SQiy-BjTW8o2x-I80D-J9o/edit?usp=sharing")
worksheet = spreadsheet.worksheet("app sheet")

# Fetch all records from the worksheet
data = worksheet.get_all_records()
                 
df = pd.DataFrame(data)

# Parse Visit Date as datetime and aggregate by month
df['Visit Date'] = pd.to_datetime(df['Visit Date'], errors='coerce')

# Create a Month column from Visit Date (as formatted "Month Year")
df['Month'] = df['Visit Date'].dt.to_period('M').dt.to_timestamp()

# Build a complete ordered list of months from the min to max Visit Date
if df['Visit Date'].notna().any():
    start = df['Visit Date'].min().to_period('M').to_timestamp()
    end = df['Visit Date'].max().to_period('M').to_timestamp()
    periods = pd.date_range(start=start, end=end, freq='MS')
    month_year_order = [p.strftime('%B %Y') for p in periods]
else:
    month_year_order = []
    df = pd.DataFrame(columns=df.columns)  # Empty DataFrame if no valid dates

# Format Month as "Month Year" and aggregate counts per month
df['Month'] = df['Month'].dt.strftime('%B %Y')
monthly_counts = df.groupby('Month').size().reindex(month_year_order, fill_value=0)
st.line_chart(monthly_counts)


st.markdown("Developed by EMTCT © Nov 2025")























































