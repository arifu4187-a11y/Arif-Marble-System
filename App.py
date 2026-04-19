import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.title("Arif Khan Marble System")

# Google Sheets Connection
conn = st.connection("gsheets", type=GSheetsConnection)

# Data Entry Form
with st.form("entry_form"):
    st.write("### Nayi Entry Karen")
    gari = st.text_input("Gari Number")
    pera = st.number_input("Pera", step=1, value=0)
    tons = st.number_input("Tons", step=0.01, value=0.0)
    cost = st.number_input("Cost (Kharcha)", step=1, value=0)
    sale = st.number_input("Sale", step=1, value=0)
    
    if st.form_submit_button("Sheet mein Save Karen"):
        # Naya data taiyar karna
        new_data = pd.DataFrame([{
            "Date": str(date.today()),
            "User": "Arif",
            "Gari": gari,
            "Pera": pera,
            "Tons": tons,
            "Cost": cost,
            "Sale": sale,
            "Profit_Loss": sale - cost
        }])
        
        # Purana data parhna aur naya jorna
        existing_data = conn.read(ttl=0)
        updated_df = pd.concat([existing_data, new_data], ignore_index=True)
        
        # Sheet update karna
        conn.update(data=updated_df)
        st.success(f"Mubarak ho Arif bhai! {gari} ka data save ho gaya.")

# Purana Record Dikhana
st.write("---")
st.write("### Aapka Pichla Record:")
try:
    df = conn.read(ttl=0)
    st.dataframe(df)
except:
    st.info("Abhi sheet mein koi data nahi hai.")
    
