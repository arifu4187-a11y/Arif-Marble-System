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
    
    submit = st.form_submit_button("Sheet mein Save Karen")
    
    if submit:
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
        
        try:
            # Mojooda data parhna
            existing_data = conn.read(ttl=0)
            if existing_data is not None and not existing_data.empty:
                updated_df = pd.concat([existing_data, new_data], ignore_index=True)
            else:
                updated_df = new_data
            
            # Sheet update karna
            conn.update(data=updated_df)
            st.success(f"Mubarak ho Arif bhai! {gari} ka data save ho gaya.")
        except Exception as e:
            st.error(f"Error: {e}")

# Record Dikhana
st.write("---")
st.write("### Aapka Record:")
try:
    df = conn.read(ttl=0)
    st.dataframe(df)
except:
    st.info("Abhi data load nahi ho raha, pehli entry save karke dekhein.")
    
