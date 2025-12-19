import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from google.oauth2 import service_account
import datetime

st.sidebar.write("""Note: Refresh the data entry page before making a new entry.""")

# Load credentials from secrets.toml
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
service_account_info = st.secrets["gcp_service_account"]
credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=scope)

# Create creds for gspread (oauth2client) compatibility
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scopes=scope)

client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open("Mentorship tool").worksheet("TA Data Entry form2")

st.header("Other TA ACTIVITIES", page_icon="Contract Edit")
st.markdown(">Please fill in the form below to submit Other activities!")


# Use session_state keys for each widget so we can reset them after submission
selected_date = st.date_input("Activity Date:", format="DD/MM/YYYY")

district_select = st.selectbox("Select District:", [" ","Bukomansimbi", "Butambala", "Gomba", "Kalungu", "Kyotera", "Lwengo", "Masaka City", "Mpigi", "Masaka Dist", "Kalangala", "Rakai", "Sembabule", "Wakiso",])


activity_venue = st.text_input("Enter activity Venue:")

list_box = st.selectbox("Select Mentor/TA Provider:", [" ", "Denis", "Mercy", "Zipporah", "Eveline", "Lilian", "Ponsiano", "Dr Zikulah"])
additional_mentor = st.text_input("If other, specify name of Mentor/TA Provider:")

topic = st.text_input("Purpose of the Activity:")
teams = st.text_area("Teams Involved:")
key_issues = st.text_area("Highlights/Findings:")
actions = st.text_area("Recommendations;Responsible persons;Timeframe:")


submitted = st.button("SUBMIT BUTTON")

# appending a row
if submitted:
    data = [
        selected_date.strftime("%d/%m/%Y") if hasattr(selected_date, "strftime") else str(selected_date),
        district_select,
        activity_venue,
        list_box,
        additional_mentor,
        topic,
        teams,
        key_issues,
        actions,
    ]
    sheet.append_row(data)
    st.success("submitted successfully!")

  


       














