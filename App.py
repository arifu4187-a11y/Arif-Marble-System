import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Page Title
st.set_page_config(page_title="Arif Khan Marble System", layout="centered")
st.title("Arif Khan Marble System")

# Secrets se data lena aur private key ko theek karna
# Ye hissa mobile par hone wali extra spaces ki galti ko saaf karta hai
service_account_info = {
    "type": "service_account",
    "project_id": st.secrets["connections"]["gsheets"]["project_id"],
    "private_key_id": st.secrets["connections"]["gsheets"]["private_key_id"],
    "private_key": st.secrets["connections"]["gsheets"]["private_key"].replace("\\n", "\n"),
    "client_email": st.secrets["connections"]["gsheets"]["client_email"],
    "client_id": st.secrets["connections"]["gsheets"]["client_id"],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": st.secrets["connections"]["gsheets"]["client_x509_cert_url"],
}

# Google Sheets se connection banana
try:
    conn = st.connection("gsheets", type=GSheetsConnection, **service_account_info)
    
    # Existing Data Load Karna
    df = conn.read(ttl=0)
    
    # Input Fields
    with st.form("entry_form"):
        st.subheader("Nayi Entry Darj Karein")
        footage = st.number_input("Footage (Sqr Ft)", min_value=0.0, format="%.2f")
        kharcha = st.number_input("Cost (Kharcha)", min_value=0)
        sale = st.number_input("Sale Price", min_value=0)
        
        submit_button = st.form_submit_button("Sheet mein Save Karen")

    if submit_button:
        if footage > 0:
            # Naya data tayyar karna
            new_data = pd.DataFrame([{
                "Footage": footage,
                "Kharcha": kharcha,
                "Sale": sale
            }])
            
            # Data update karna
            updated_df = pd.concat([df, new_data], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Mubarak ho! Record sahi se save ho gaya hai.")
            st.rerun()
        else:
            st.warning("Meherbani karke footage darj karein.")

    # Record dikhane ke liye
    st.divider()
    st.subheader("Aapka Record:")
    if not df.empty:
        st.dataframe(df.tail(10)) # Sirf aakhri 10 entries
    else:
        st.info("Abhi data load nahi ho raha, pehli entry save karke dekhein.")

except Exception as e:
    st.error(f"Error: {e}")
    
