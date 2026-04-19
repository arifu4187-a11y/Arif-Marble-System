import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Arif Khan Marble System")

# Google Sheet se connect karne ka naya tarika
conn = st.connection("gsheets", type=GSheetsConnection)

# Data read karna
df = conn.read()
st.write("Aapka Data:", df)

# Data save karne ka button
if st.button("Sheet mein Save Karen"):
    # Yahan save karne ka logic aayega
    st.success("Data Save Ho Gaya!")
    
