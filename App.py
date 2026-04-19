import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Arif Khan Marble System")

# Connection setup
conn = st.connection("gsheets", type=GSheetsConnection)

# Form for entry
with st.form("entry_form"):
    gari = st.text_input("Gari Number")
    tons = st.number_input("Tons", step=0.01)
    cost = st.number_input("Cost", step=1)
    submit = st.form_submit_button("Sheet mein Save Karen")

    if submit:
        # Naya data taiyar karna
        new_row = pd.DataFrame([{"Gari": gari, "Tons": tons, "Cost": cost}])
        
        # Purana data parhna aur naya shamil karna
        existing_data = conn.read(ttl=0)
        updated_df = pd.concat([existing_data, new_row], ignore_index=True)
        
        # Sheet mein wapas bhejna
        conn.update(data=updated_df)
        st.success("Mubarak ho! Data save ho gaya.")
        
