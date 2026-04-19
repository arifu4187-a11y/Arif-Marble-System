import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Arif Khan Marble System")
st.title("Arif Khan Marble System")

# Google Sheet Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Login System
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    user = st.text_input("User Name")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if user == "arif" and password == "1234":
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Ghalat Password!")
else:
    # Data Entry Form
    with st.form("entry_form"):
        date = st.date_input("Tareekh")
        gari = st.text_input("Gari Number")
        pera = st.number_input("Pera", step=1)
        tons = st.number_input("Tons", step=0.01)
        cost = st.number_input("Kharcha (Cost)", step=1)
        sale = st.number_input("Sale", step=1)
        
        if st.form_submit_button("Sheet mein Save Karen"):
            new_data = pd.DataFrame([{
                "Date": str(date),
                "User": "Arif",
                "Gari": gari,
                "Pera": pera,
                "Tons": tons,
                "Cost": cost,
                "Sale": sale,
                "Profit_Loss": sale - cost
            }])
            
            existing_data = conn.read()
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_data)
            st.success("Data Save Ho Gaya!")

    # Show Data
    st.write("### Purana Record:")
    data = conn.read()
    st.dataframe(data)
    
