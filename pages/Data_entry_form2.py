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
st.set_page_config(page_title="Material Icons Example", page_icon="<svg xmlns="http://www.w3.org/2000/svg" height="48px" viewBox="0 -960 960 960" width="48px" fill="#4B77D1"><path d="M360-640v-60h360v60H360Zm0 120v-60h360v60H360Zm140 380H180h320Zm0 60H225q-43.75 0-74.37-30.63Q120-141.25 120-185v-135h120v-560h600v381q-15-2-30.37-.03-15.38 1.97-29.63 7.03v-328H300v500h292l-60 60H180v75q0 19.12 13 32.06Q206-140 224-140h276v60Zm60 0v-123l221-220q9-9 20-13t22-4q12 0 23 4.5t20 13.5l37 37q9 9 13 20t4 22q0 11-4.5 22.5T902.09-300L683-80H560Zm300-263-37-37 37 37ZM620-140h38l121-122-18-19-19-18-122 121v38Zm141-141-19-18 37 37-18-19Z"/></svg>")
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

  


       














