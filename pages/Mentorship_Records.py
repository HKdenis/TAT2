import streamlit as st
import pandas as pd
import plotly.express as px
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2 import service_account

st.subheader("MENTORSHIP RECORDS")

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

st.dataframe(df, use_container_width=True)
st.markdown("### DISTRIBUTION OF MENTORSHIP VISITS BY DIFFERENT CATEGORIES")
st.markdown("MENTOR/TA PROVIDER")
st.plotly_chart(px.histogram(df, x="Mentor/ TA Provider"), use_container_width=True)
st.markdown("DISTRICT")
st.plotly_chart(px.histogram(df, x="District"), use_container_width=True)
st.markdown("HEALTH FACILITY")
st.plotly_chart(px.histogram(df, x="Health Facility"), use_container_width=True)
