import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.title("Arif Khan Marble System")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0)
    
    with st.form("entry_form"):
        footage = st.number_input("Footage", min_value=0.0)
        kharcha = st.number_input("Kharcha", min_value=0)
        sale = st.number_input("Sale", min_value=0)
        submit = st.form_submit_button("Save Karen")

    if submit:
        new_row = pd.DataFrame([{"Footage": footage, "Kharcha": kharcha, "Sale": sale}])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        conn.update(data=updated_df)
        st.success("Save ho gaya!")
        st.rerun()

    st.dataframe(df)
except Exception as e:
    st.error(f"Masla: {e}")
    
