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

st.header("***OTHER TA ACTIVITIES***")
st.markdown(">Please fill in the form below to submit Other activities!")


# Use session_state keys for each widget so we can reset them after submission
selected_date = st.date_input("ACTIVITY DATE:", format="DD/MM/YYYY")

district_select = st.selectbox("SELECT DISTRICT IF APPLICABLE:", [" ","Bukomansimbi", "Butambala", "Gomba", "Kalungu", "Kyotera", "Lwengo", "Masaka City", "Mpigi", "Masaka Dist", "Kalangala", "Rakai", "Sembabule", "Wakiso",])

facility_select = st.selectbox("HEALTH FACILITY IF APPLICABLE:", [" ","Bigasa Health center III", "Butenga Health center III", "Kagoggo Health Centre II", "Kigangazzi Health Centre II",
"Kisojjo Health Centre II", "Kitanda Health Centre III", "Mirambi Health Centre III", "St. Mary's Maternity & Nursing Home", "Bulo Health Centre III", "Butaaka Health Centre III", "Epi-CentreSenge Health Centre", 
"Kalamba Community Health Centre II", "Kibugga Health Centre II", "Kitimba Health Centre III", "Kiziiko Health Centre II", "Kyabadaza Health Centre III", "Ngando Health Centre III","Gombe General Hospital",
"Bulwadda Health Centre III", "Buyanja Health Centre II", "Kanoni Health Centre III", "Kifampa Health Centre III", "Kisozi Health Centre III", "Kitwe Health Centre II", "Kyayi Health Centre III", "Maddu Health Centre", 
"Ngomanene Health Centre III", "Bubeke Health Centre III", "Bufumira Health Centre III", "Bukasa Health Centre IV", "Bwendero Health Centre III", "Jaana Health Centre II", "Kachanga Island Health Centre II",
"Mulabana Health Centre II", "Ssese Islands African Aids Project Health Centre II", "AHF Uganda Care", "Bukulula Health Centre IV", "Kabaale Health Centre III", "Kalungu Health Centre III", "Kasambya Health centre", 
"MRC Kyamulibwa Health Centre II", "Nabutongwa Health Centre II", "Kabira Health Centre III", "Kabuwoko Govt Health Centre III", "Kakuuto Health Centre IV", "Kalisizo General Hospital", "Kasaali Health Centre", 
"Mitukula Health Centre III", "Mutukula Health Centre III", "Nabigasa Health Centre III", "Ndolo Health Centre II", "Rakai Health Sciences Program Clinic", "Kakoma Health Centre III", "Katovu Health Centre",
"Kiwangala Health Centre IV","Kabayanda Health Centre II", "Kaliiro Health Centre III", "Kasagama Health Centre III", "Kinuuka Health Centre III", "Kyemamba Health Centre II", "Lyakajura Health Centre III", "Lyantonde General Hospital", 
"Masaka Municipal Clinic", "Masaka Police Health Centre III", "Mpugwe Health Centre III", "Nyendo Health Centre III", "TASO Masaka", "Bukakata Health Centre III",
"Bukeeri Health Centre III", "Buwunga Health Centre III", "Buyaga Health Centre II", "Kamulegu Health Centre III", "Kyanamukaaka Health Centre IV", "Bujuuko Health Centre III", "Bukasa Health Centre II", 
"Buwama Health Centre III", "Buyiga Health Centre III", "Dona Carnevale Medical Centre", "Fiduga Medical Centre", "Ggolo Health Centre III","Butoolo Health centre III", 
"Kampiringisa Health Centre III", "Kiringente Epi Health Centre II", "Kituntu Health Centre III", "Mpigi Health Centre IV", "Muduuma Health Centre III", "Nabyewanga Health Centre II", "Nindye Health Centre",
 "Nsamu/Kyali Health Centre III", "Sekiwunga Health Centre III", "St. Elizabeth Kibanga Ihu Health Centre III", "Bugona Health Centre II",
"Butiti Health Centre II", "Buyamba Health Centre III", "Byakabanda Health Centre III", "Kacheera Health Centre III",
"Kasankala Health Centre II", "Kayonza Kacheera Health Centre II", "Kibaale Health Centre II", "Kibanda Health Centre III",
"Kibuuka Health Centre II", "Kifamba Health Centre III", "Kimuli Health Centre III", "Kyabigondo Health Centre II", "Kyalulangira Health Centre III",
"Lwabakooba Health Centre II", "Lwakalolo Health Centre II", "Lwamaggwa Govt Health Centre III", "Lwanda Health Centre III", "Lwembajjo Health Centre II",
"Magabi Health Centre II", "Rakai General Hospital", "Rakai Kiziba Health Centre III", "Busheka (Sembabule) Health Centre III",
"Kabundi Health Centre II", "Kayunga Health Centre II", "Kyabi Health Centre III", "Kyeera Health Centre III", "Lugusulu Health Centre III", "Lwebitakuli Gvt Health Centre IV",
"Lwemiyaga Health Centre III", "Makoole Health Centre II", "Mateete Health Centre III", "Mitima Health Centre II",
"Ntete Health Centre III", "Ntuusi Health Centre IV", "Sembabule Kabaale Health Centre II", "Ssembabule Health Centre IV",
"Bulondo Health Centre III", "Bunamwaya Health Centre II", "Busawamanze Health Centre III", "Bussi Health Centre III", "Buwambo Health Centre IV",
"Bweyogerere Health Centre III", "Community Health Plan Uganda", "Ggwatiro Nursing Home Hospital", "Gombe (Wakiso) Health Centre II",
"Joint Clinical Research Centre", "Kabubbu Health Centre IV", "Kajjansi Health Centre IV", "Kakiri Health Centre III",
"Kasangati Health Centre IV", "Kasanje Health Centre III", "Kasenge Health Centre II", "Kasoozo Health Centre III",
"Katabi Health Centre III", "Kawanda Health Centre III", "Kigungu Health Centre III", "Kimwanyi Health Centre II",
"Kira Health Centre IV", "Kireka Health Centre III", "Kirinya Health Centre III", "Kitala Health Centre II",
"Kiziba Health Centre III", "Kyengera Health Centre III", "Kyengeza Health Centre II", "Lubbe Health Centre II",
"Lufuka Valley Health Centre III", "Maganjo Health Centre II", "Magoggo Health Centre II", "Matuga Health Centre III",
"Mende Health Centre III", "Migadde Health Centre II", "Mildmay Uganda Hospital", "Mutundwe Health Centre II", "Mutungo Health Centre II",
"Nabutiti Health Centre III", "Nabweru Health Centre III", "Nakawuka Health Centre III", "Nakitokolo Namayumba Health Centre III",
"Nalugala Health Centre II", "Namayumba Epi Health Centre III", "Namayumba Health Centre IV", "Namugongo Fund for Special Children Clinic",
"Namulonge Health Centre III", "Nansana Health Centre II", "Nassolo Wamala Health Centre III", "Ndejje Health Centre IV",
"Nsaggu Health Centre II", "Nsangi Health Centre III", "Nurture Africa Clinic", "Seguku Health Centre II",
"TASO Entebbe", "Triam Medical Health Centre II", "Ttikalu Health Centre III", "Wagagai Health Centre IV",
"Wakiso Banda Health Centre II", "Wakiso EPI Health Centre III", "Wakiso Health Centre IV",
"Wakiso Kasozi Health Centre III", "Watubba Health Centre III", "Zzinga Health Centre III"])

Office = st.text_input("Enter activity Venue[If not at a Health Facility]:")

list_box = st.selectbox("Select Mentor/TA Provider:", [" ", "Denis", "Mercy", "Zipporah", "Eveline", "Lilian", "Ponsiano", "Dr Zikulah"])
additional_mentor = st.text_input("If other, specify name of Mentor/TA Provider:")

topic = st.text_input("Purpose of the Activity:")
teams = st.text_area("Teams Involved:")
key_issues = st.text_area("Highlights/Findings:")
actions = st.text_area("Recommendations;Responsible persons;Timeframe:")


submitted = st.button("SUBMIT")

# appending a row
if submitted:
    data = [
        selected_date.strftime("%d/%m/%Y") if hasattr(selected_date, "strftime") else str(selected_date),
        district_select,
        facility_select,
        office,
        list_box,
        additional_mentor,
        topic,
        teams,
        key_issues,
        actions,
    ]
    sheet.append_row(data)
    st.success("submitted successfully!")


    
 # 


       














